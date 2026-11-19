"""Controla OWASP ZAP (modo daemon) por su API para el laboratorio de la Evaluación 3.

Uso:
  ZAP_API_KEY=... python zap_lab.py sesion <nombre>          # sesión nueva + contexto limitado al CRUD
  ZAP_API_KEY=... python zap_lab.py esperar                   # espera a que termine el análisis pasivo
  ZAP_API_KEY=... python zap_lab.py reporte <carpeta> <titulo> # HTML, JSON y MD filtrados al objetivo + URLs visitadas
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ZAP = "http://127.0.0.1:8090"
OBJETIVO = "http://127.0.0.1:8000"
CONTEXTO = "CRUD-laboratorio"


def api(ruta, **params):
    params["apikey"] = os.environ["ZAP_API_KEY"]
    url = f"{ZAP}/JSON/{ruta}/?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def sesion(nombre):
    api("core/action/newSession", name=nombre, overwrite="true")
    api("context/action/newContext", contextName=CONTEXTO)
    api("context/action/includeInContext", contextName=CONTEXTO, regex=r"http://127\.0\.0\.1:8000.*")
    print(f"Sesión '{nombre}' creada; contexto '{CONTEXTO}' incluye solo {OBJETIVO}")


def esperar():
    while int(api("pscan/view/recordsToScan")["recordsToScan"]) > 0:
        time.sleep(2)
    print("Análisis pasivo terminado.")


def reporte(carpeta, titulo):
    carpeta = os.path.abspath(carpeta)
    os.makedirs(carpeta, exist_ok=True)
    for plantilla, nombre in [("traditional-html", "reporte.html"), ("traditional-json", "reporte.json"), ("traditional-md", "reporte.md")]:
        api("reports/action/generate", title=titulo, template=plantilla, sites=OBJETIVO,
            contexts=CONTEXTO, reportDir=carpeta, reportFileName=nombre)
    urls = api("core/view/urls", baseurl=OBJETIVO)["urls"]
    with open(os.path.join(carpeta, "urls_visitadas.txt"), "w") as f:
        f.write(f"# URLs del objetivo registradas por ZAP ({len(urls)}), {time.strftime('%Y-%m-%d %H:%M %z')}\n")
        f.write("\n".join(sorted(urls)) + "\n")
    sitios = api("core/view/sites")["sites"]
    with open(os.path.join(carpeta, "arbol_sites.txt"), "w") as f:
        f.write("# Todos los sitios del árbol Sites de ZAP (los ajenos a 127.0.0.1:8000 no son el CRUD)\n")
        f.write("\n".join(sitios) + "\n")
    print(f"Reportes en {carpeta}: {len(urls)} URLs del objetivo, {len(sitios)} sitios en el árbol")


if __name__ == "__main__":
    comando, *args = sys.argv[1:]
    {"sesion": sesion, "esperar": esperar, "reporte": reporte}[comando](*args)
