"""Construye el informe en Word sobre la plantilla institucional (Carta-1-vert.docx) a partir de informe.html.

Conserva portada, encabezado, pie y contraportada de la plantilla; reemplaza el contenido de ejemplo
replicando su formato (Tahoma, títulos rojos EE0000 de 18 pt, subtítulos de 14 pt, texto de 11 pt).

Uso: python generar_docx.py <plantilla.docx> <informe.html> <salida.docx> <dir_trabajo>
"""
import html
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile
from html.parser import HTMLParser

PLANTILLA, HTML_IN, SALIDA, TRABAJO = sys.argv[1:5]
BASE_HTML = os.path.dirname(os.path.abspath(HTML_IN))
ANCHO = 12240 - 2 * 851            # ancho útil en DXA (twips)
EMU_POR_DXA = 635
ROJO = "EE0000"
FONT = '<w:rFonts w:ascii="Tahoma" w:hAnsi="Tahoma" w:cs="Tahoma"/>'
MONO = '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>'


# ------------------------------------------------------------------ árbol HTML mínimo
class Nodo:
    def __init__(self, tag, attrs=None, padre=None):
        self.tag, self.attrs, self.padre, self.hijos = tag, dict(attrs or {}), padre, []

    def texto(self):
        return "".join(h if isinstance(h, str) else h.texto() for h in self.hijos)

    def clase(self):
        return self.attrs.get("class", "") or ""


class Arbol(HTMLParser):
    VACIOS = {"img", "br", "meta", "hr", "path", "line", "rect"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = Nodo("raiz")
        self.actual = self.raiz
        self.svg = []          # texto bruto de cada <svg>

    def handle_starttag(self, tag, attrs):
        n = Nodo(tag, attrs, self.actual)
        self.actual.hijos.append(n)
        if tag not in self.VACIOS:
            self.actual = n

    def handle_endtag(self, tag):
        n = self.actual
        while n is not self.raiz and n.tag != tag:
            n = n.padre
        if n is not self.raiz:
            self.actual = n.padre

    def handle_data(self, data):
        self.actual.hijos.append(data)


# ------------------------------------------------------------------ OOXML
def esc(t):
    return html.escape(t, quote=False)


def run(texto, tam=22, bold=False, ital=False, color=None, mono=False, under=False, shade=None):
    rpr = (MONO if mono else FONT)
    rpr += "<w:b/>" if bold else ""
    rpr += "<w:i/>" if ital else ""
    rpr += f'<w:color w:val="{color}"/>' if color else ""
    rpr += f'<w:sz w:val="{tam}"/><w:szCs w:val="{tam}"/>'
    rpr += '<w:u w:val="single"/>' if under else ""
    rpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
    partes = texto.split("\n")
    out = []
    for i, p in enumerate(partes):
        if i:
            out.append(f"<w:r><w:rPr>{rpr}</w:rPr><w:br/></w:r>")
        if p:
            out.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{esc(p)}</w:t></w:r>')
    return "".join(out)


class Doc:
    def __init__(self):
        self.cuerpo = []
        self.rels = []          # (rId, tipo, target, externo)
        self.medios = []        # (nombre, ruta)
        self.n_rel = 100
        self.n_img = 0

    def rel(self, tipo, target, externo=False):
        self.n_rel += 1
        rid = f"rIdU3{self.n_rel}"
        self.rels.append((rid, tipo, target, externo))
        return rid

    # --- inline: nodo HTML -> runs
    def runs(self, nodo, tam=22, bold=False, ital=False, color=None, mono=False):
        out = []
        for h in nodo.hijos:
            if isinstance(h, str):
                t = re.sub(r"\s+", " ", h)
                if t:
                    out.append(run(t, tam, bold, ital, color, mono, shade="F2F2F2" if mono else None))
                continue
            tag, cls = h.tag, h.clase()
            if tag in ("b", "strong"):
                out.append(self.runs(h, tam, True, ital, color, mono))
            elif tag in ("i", "em"):
                out.append(self.runs(h, tam, bold, True, color, mono))
            elif tag == "code":
                out.append(self.runs(h, max(tam - 3, 14), bold, ital, color, True))
            elif tag == "span" and "good" in cls:
                out.append(self.runs(h, tam, True, ital, "1F7A5A", mono))
            elif tag == "span" and "bad" in cls:
                out.append(self.runs(h, tam, True, ital, "B8452F", mono))
            elif tag == "a":
                rid = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", h.attrs["href"], True)
                out.append(f'<w:hyperlink r:id="{rid}">{run(h.texto(), tam, bold, ital, "0563C1", mono, under=True)}</w:hyperlink>')
            elif tag == "br":
                out.append(run("\n", tam))
            else:
                out.append(self.runs(h, tam, bold, ital, color, mono))
        return "".join(out)

    # --- bloques
    def p(self, contenido, jc=None, antes=0, despues=120, keep=False, ind=None, shade=None):
        # Orden exigido por el esquema de Word: keepNext, shd, spacing, ind, jc.
        ppr = "<w:keepNext/>" if keep else ""
        ppr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
        ppr += f'<w:spacing w:before="{antes}" w:after="{despues}"/>'
        ppr += ind or ""
        ppr += f'<w:jc w:val="{jc}"/>' if jc else ""
        return f"<w:p><w:pPr>{ppr}</w:pPr>{contenido}</w:p>"

    def titulo1(self, texto):
        self.cuerpo.append(self.p(run(texto, 36, color=ROJO), jc="center", antes=360, despues=180, keep=True))

    def titulo2(self, texto):
        self.cuerpo.append(self.p(run(texto, 28, color=ROJO), antes=240, despues=120, keep=True))

    def parrafo(self, nodo, tam=22):
        jc = "both" if tam >= 20 else None
        self.cuerpo.append(self.p(self.runs(nodo, tam), jc=jc))

    def vinetas(self, ul):
        for li in [h for h in ul.hijos if not isinstance(h, str) and h.tag == "li"]:
            self.cuerpo.append(self.p(run("‐ ") + self.runs(li), despues=60,
                                      ind='<w:ind w:left="284" w:hanging="284"/>'))

    def codigo(self, texto, titulo=None):
        if titulo:
            self.cuerpo.append(self.p(run(titulo, 18, bold=True, color="35607D"), antes=120, despues=40, keep=True))
        self.cuerpo.append(self.p(run(texto.strip("\n"), 15, mono=True), despues=160, shade="F2F2F2"))

    def imagen_xml(self, ruta, ancho_dxa):
        with open(ruta, "rb") as f:
            cab = f.read(32)
        if cab[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", cab[16:24])
        else:
            raise SystemExit(f"Solo PNG: {ruta}")
        self.n_img += 1
        nombre = f"u3_img{self.n_img}.png"
        self.medios.append((nombre, ruta))
        rid = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", f"media/{nombre}")
        cx = int(ancho_dxa * EMU_POR_DXA)
        cy = int(cx * h / w)
        max_cy = int(8.6 * 914400)            # no más alto que ~22 cm
        if cy > max_cy:
            cx, cy = int(cx * max_cy / cy), max_cy
        pid = 5000 + self.n_img
        return (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
                f'<wp:docPr id="{pid}" name="Imagen {pid}"/><wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
                f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
                f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{pid}" name="{nombre}"/><pic:cNvPicPr/></pic:nvPicPr>'
                f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
                f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')

    def figura(self, fig, ancho_dxa=ANCHO, devolver=False):
        img = next(h for h in fig.hijos if not isinstance(h, str) and h.tag == "img")
        ruta = os.path.normpath(os.path.join(BASE_HTML, img.attrs["src"]))
        pct = re.search(r"width:\s*(\d+)%", img.attrs.get("style", ""))
        ancho = int(ancho_dxa * (int(pct.group(1)) / 100 if pct else 1))
        cap = next((h for h in fig.hijos if not isinstance(h, str) and h.tag == "figcaption"), None)
        xml = self.p(self.imagen_xml(ruta, ancho), jc="center", antes=120, despues=40, keep=True)
        if cap is not None:
            xml += self.p(self.runs(cap, 17, ital=True, color="5C6B66"), jc="center", despues=160)
        if devolver:
            return xml
        self.cuerpo.append(xml)

    def tabla(self, nodo, tam=None):
        filas = []
        for tr in nodo.iter_tr():
            celdas = [c for c in tr.hijos if not isinstance(c, str) and c.tag in ("td", "th")]
            filas.append(celdas)
        if not filas:
            return
        ncol = max(len(f) for f in filas)
        cls = nodo.clase()
        tam = tam or (15 if "xs" in cls else 17 if "small" in cls else 18)
        largos = [max(min(len(f[i].texto()) if i < len(f) else 0, 60) for f in filas) + 6 for i in range(ncol)]
        total = sum(largos)
        # Mínimo por columna: que quepa su palabra más larga sin cortarse (aprox. 0,58 em por carácter).
        por_caracter = tam * 10 * 0.58
        def palabra_mas_larga(i):
            return max((len(w) for f in filas if i < len(f) for w in f[i].texto().split()), default=4)
        # shortcut: las palabras de más de 12 caracteres (URLs, cabeceras) pueden partirse; así no aplastan otras columnas.
        minimos = [int(min(palabra_mas_larga(i), 12) * por_caracter) + 160 for i in range(ncol)]
        if sum(minimos) > ANCHO * 0.9:
            minimos = [int(m * ANCHO * 0.9 / sum(minimos)) for m in minimos]
        anchos = [max(int(ANCHO * l / total), m) for l, m in zip(largos, minimos)]
        exceso = sum(anchos) - ANCHO
        if exceso > 0:                      # se descuenta de las columnas con holgura sobre su mínimo
            ajustables = sum(a - m for a, m in zip(anchos, minimos)) or 1
            anchos = [a - int(exceso * (a - m) / ajustables) for a, m in zip(anchos, minimos)]
        anchos[-1] += ANCHO - sum(anchos)
        bordes = "".join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
        xml = [f'<w:tbl><w:tblPr><w:tblW w:w="{ANCHO}" w:type="dxa"/><w:tblBorders>{bordes}</w:tblBorders>'
               f'<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="70" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar></w:tblPr>'
               f'<w:tblGrid>{"".join(f"<w:gridCol w:w=\"{a}\"/>" for a in anchos)}</w:tblGrid>']
        for r, f in enumerate(filas):
            enc = all(c.tag == "th" for c in f)
            xml.append("<w:tr>" + ('<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' if enc else "<w:trPr><w:cantSplit/></w:trPr>"))
            for i, c in enumerate(f):
                fill = ROJO if enc else ("F7F7F7" if r % 2 == 0 else "FFFFFF")
                cont = self.runs(c, tam, bold=enc, color="FFFFFF" if enc else None)
                xml.append(f'<w:tc><w:tcPr><w:tcW w:w="{anchos[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>'
                           f'{self.p(cont or run(" ", tam), despues=0)}</w:tc>')
            xml.append("</w:tr>")
        xml.append("</w:tbl>")
        self.cuerpo.append("".join(xml))
        self.cuerpo.append(self.p("", despues=80))

    def doble(self, figs):
        """Dos figuras lado a lado en una tabla sin bordes."""
        mitad = ANCHO // 2
        celdas = "".join(f'<w:tc><w:tcPr><w:tcW w:w="{mitad}" w:type="dxa"/></w:tcPr>{self.figura(f, mitad - 120, True)}</w:tc>' for f in figs)
        self.cuerpo.append(f'<w:tbl><w:tblPr><w:tblW w:w="{ANCHO}" w:type="dxa"/><w:tblLayout w:type="fixed"/></w:tblPr>'
                           f'<w:tblGrid><w:gridCol w:w="{mitad}"/><w:gridCol w:w="{mitad}"/></w:tblGrid><w:tr>{celdas}</w:tr></w:tbl>')


def iter_tr(self):
    for h in self.hijos:
        if isinstance(h, str):
            continue
        if h.tag == "tr":
            yield h
        elif h.tag in ("thead", "tbody"):
            yield from h.iter_tr()


Nodo.iter_tr = iter_tr


# ------------------------------------------------------------------ recorrido del HTML
def svg_a_png(svg, destino):
    pagina = os.path.join(TRABAJO, "diagrama.html")
    estilo = (".t{font:bold 12px Arial;text-anchor:middle;fill:#0F3D2E}.s{font:10px Arial;text-anchor:middle;fill:#5C6B66}"
              ".z{font:bold 11px Arial;fill:#35607D}")
    with open(pagina, "w") as f:
        f.write(f"<html><body style='margin:0;background:#fff'><style>{estilo}</style>"
                f"<div style='width:1800px'>{svg.replace('class=\"diagrama\"', 'width=\"1800\" height=\"500\"')}</div></body></html>")
    subprocess.run(["chromium", "--headless=new", "--hide-scrollbars", "--window-size=1800,500",
                    f"--screenshot={destino}", f"file://{pagina}"], check=True, capture_output=True)


def recorrer(doc, nodo, svgs):
    hijos = [h for h in nodo.hijos if not isinstance(h, str) or h.strip()]
    i = 0
    while i < len(hijos):
        h = hijos[i]
        i += 1
        if isinstance(h, str):
            continue
        tag, cls = h.tag, h.clase()
        if tag == "section" and "portada" in cls:
            continue
        if tag == "h2":
            doc.titulo1(re.sub(r"^(\d+)\.\s*", r"\1 ", h.texto()))
        elif tag == "h3":
            doc.titulo2(h.texto())
        elif tag == "p":
            doc.parrafo(h, 18 if "small" in cls else 22)
        elif tag == "ul":
            doc.vinetas(h)
        elif tag == "table":
            doc.tabla(h)
        elif tag == "figure":
            doc.figura(h)
        elif tag == "div" and "code-title" in cls:
            pre = hijos[i]
            i += 1
            doc.codigo(pre.texto(), h.texto())
        elif tag == "pre":
            doc.codigo(h.texto())
        elif tag == "div" and "grid2" in cls:
            figs = [x for x in h.hijos if not isinstance(x, str) and x.tag == "figure"]
            if len(figs) == 2:
                doc.doble(figs)
            else:
                recorrer(doc, h, svgs)
        elif tag == "svg":
            destino = os.path.join(TRABAJO, "diagrama.png")
            svg_a_png(svgs.pop(0), destino)
            doc.cuerpo.append(doc.p(doc.imagen_xml(destino, ANCHO), jc="center", antes=120, despues=120))
        else:
            recorrer(doc, h, svgs)


def main():
    fuente = open(HTML_IN, encoding="utf-8").read()
    svgs = re.findall(r"<svg.*?</svg>", fuente, re.S)
    arbol = Arbol()
    arbol.feed(fuente)
    body = next(h for h in arbol.raiz.hijos if not isinstance(h, str) and h.tag == "html")
    body = next(h for h in body.hijos if not isinstance(h, str) and h.tag == "body")
    doc = Doc()
    recorrer(doc, body, svgs)

    # --- plantilla
    dst = os.path.join(TRABAJO, "salida")
    shutil.rmtree(dst, ignore_errors=True)
    with zipfile.ZipFile(PLANTILLA) as z:
        z.extractall(dst)
    ruta_doc = os.path.join(dst, "word", "document.xml")
    x = open(ruta_doc, encoding="utf-8").read()
    ini_body = x.index("<w:body>") + len("<w:body>")
    fin_body = x.index("</w:body>")
    parrafos = re.findall(r"<w:p(?:\s[^>]*)?/>|<w:p(?:\s[^>]*)?>.*?</w:p>", x[ini_body:fin_body], re.S)
    sect = re.search(r"<w:sectPr.*?</w:sectPr>", x[ini_body:fin_body], re.S).group(0)

    portada = []
    for p in parrafos[:9]:
        if "TITULO PORTADA TRABAJO" in p:
            p = p.replace("TITULO PORTADA TRABAJO", "INFORME TÉCNICO · EVALUACIÓN Nº 3")
        if "Ejemplo de subtítulo" in p:
            p = p.replace("Ejemplo de subtítulo", "CRUD Django con login, Docker y OWASP ZAP")
        if "NOMBRE:" in p:
            p = (p.replace("<w:t>NOMBRE:</w:t>", "<w:t xml:space=\"preserve\">NOMBRES: Xavier Romero · Alejandro Figueroa</w:t>")
                  .replace("<w:t xml:space=\"preserve\">CARRERA: </w:t>", "<w:t xml:space=\"preserve\">CARRERA: </w:t>")
                  .replace("<w:t xml:space=\"preserve\">ASIGNATURA: </w:t>", "<w:t xml:space=\"preserve\">ASIGNATURA: Desarrollo Seguro</w:t>")
                  .replace("<w:t>PROFESOR:</w:t>", "<w:t xml:space=\"preserve\">PROFESOR: </w:t>")
                  .replace("<w:t>FECHA:</w:t>", "<w:t xml:space=\"preserve\">FECHA: 19-11-2026</w:t>"))
        portada.append(p)
    contraportada = [p for p in parrafos if "<w:drawing" in p]
    salto = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
    vacio = "<w:p/>"
    nuevo = "".join(portada) + salto + "".join(doc.cuerpo) + salto + vacio * 6 + "".join(contraportada) + sect
    x = x[:ini_body] + nuevo + x[fin_body:]
    open(ruta_doc, "w", encoding="utf-8").write(x)

    # --- medios y relaciones
    os.makedirs(os.path.join(dst, "word", "media"), exist_ok=True)
    for nombre, ruta in doc.medios:
        shutil.copy(ruta, os.path.join(dst, "word", "media", nombre))
    ruta_rels = os.path.join(dst, "word", "_rels", "document.xml.rels")
    rels = open(ruta_rels, encoding="utf-8").read()
    extra = "".join(f'<Relationship Id="{rid}" Type="{tipo}" Target="{html.escape(t)}"{" TargetMode=\"External\"" if ext else ""}/>'
                    for rid, tipo, t, ext in doc.rels)
    open(ruta_rels, "w", encoding="utf-8").write(rels.replace("</Relationships>", extra + "</Relationships>"))
    ct = os.path.join(dst, "[Content_Types].xml")
    c = open(ct, encoding="utf-8").read()
    if 'Extension="png"' not in c:
        c = c.replace("<Types ", "<Types ", 1).replace("<Default ", '<Default Extension="png" ContentType="image/png"/><Default ', 1)
    open(ct, "w", encoding="utf-8").write(c)
    core = os.path.join(dst, "docProps", "core.xml")
    k = open(core, encoding="utf-8").read()
    k = re.sub(r"<dc:title>.*?</dc:title>|<dc:title/>", "<dc:title>Informe Evaluación 3 - Desarrollo Seguro</dc:title>", k)
    open(core, "w", encoding="utf-8").write(k)

    if os.path.exists(SALIDA):
        os.remove(SALIDA)
    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, _, archivos in os.walk(dst):
            for a in archivos:
                completo = os.path.join(raiz, a)
                z.write(completo, os.path.relpath(completo, dst))
    print("OK", SALIDA, f"{len(doc.cuerpo)} bloques, {doc.n_img} imágenes, {len(doc.rels)} relaciones")


if __name__ == "__main__":
    main()
