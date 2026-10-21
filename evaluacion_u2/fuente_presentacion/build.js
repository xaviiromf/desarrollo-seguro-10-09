// Generador de la presentación Evaluación U2 — Desarrollo Seguro.
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa6");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";
const GUION = require(__dirname + "/guion.json");
let NOTA = 0;
function notas() {
  const g = GUION[NOTA++];
  let t = g.partes.map((p) => `[${p.quien} · ${p.seg} s]\n${p.decir}`).join("\n\n");
  t += (t ? "\n\n" : "") + "HACER: " + g.hacer.join(" · ");
  if (g.demo) t += "\nDEMO (terminal en la raíz del proyecto, venv activo): " + g.demo;
  if (g.fuentes) t += "\n\nFuente (no leer): " + g.fuentes;
  return t;
}

const THEME = {
  name: "Desarrollo Seguro U2",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2B26", lt1: "FFFFFF", dk2: "0F3D2E", lt2: "EEF5F1",
    accent1: "1F7A5A", accent2: "D9922E", accent3: "B8452F", accent4: "35607D",
    accent5: "9CCBB4", accent6: "5C6B66", hlink: "1F7A5A", folHlink: "35607D",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.author = "Xavier Romero y Alejandro Figueroa";
pres.title = "Revisión de seguridad del CRUD Supermercado";
pres.subject = "Desarrollo Seguro, Unidad 2";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333, MX = 0.6, CW = W - 2 * MX;
const FOOT = "Desarrollo Seguro · Unidad 2 · Xavier Romero y Alejandro Figueroa · 22-10-2026";

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 2.2, w: 8.4, h: 1.9, fontSize: 44, bold: true, color: C.background1, valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: MX, y: 4.2, w: 8.4, h: 0.9, fontSize: 20, color: C.accent5, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CIERRE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 1.1, w: CW, h: 1.0, fontSize: 34, bold: true, color: C.background1, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: C.background1 },
  margin: [0.5, 0.6, 0.7, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: MX, y: 0.35, w: CW, h: 0.8, fontSize: 32, bold: true, color: C.text2, valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: MX, y: 7.02, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

// ---------- Helpers ----------
async function iconPng(Comp, hex) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + hex, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}
const ICONS = {};
async function loadIcons() {
  const want = {
    shield: fa.FaShieldHalved, cart: fa.FaCartShopping, form: fa.FaPenToSquare, scope: fa.FaMagnifyingGlass,
    user: fa.FaUser, check: fa.FaCheck, xmark: fa.FaXmark, warn: fa.FaTriangleExclamation, key: fa.FaKey,
    globe: fa.FaGlobe, clock: fa.FaClock, bullhorn: fa.FaBullhorn, flask: fa.FaFlask, code: fa.FaCode,
    box: fa.FaBoxOpen, server: fa.FaServer, scale: fa.FaScaleBalanced, clip: fa.FaClipboardCheck,
    db: fa.FaDatabase, list: fa.FaListCheck, gauge: fa.FaGaugeHigh, cube: fa.FaCubes,
    link: fa.FaLink, lightbulb: fa.FaLightbulb, file: fa.FaFileLines,
  };
  for (const [k, Comp] of Object.entries(want)) ICONS[k] = await iconPng(Comp, "FFFFFF");
}

function txt(slide, text, o) {
  slide.addText(text, Object.assign({ isTextBox: true, margin: 0, valign: "top", fontSize: 14, color: C.text1 }, o));
}
function card(slide, x, y, w, h, fill, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, fill: { color: fill || C.background2 }, line: { type: "none" },
    shadow: { type: "outer", color: "000000", opacity: 0.10, blur: 6, offset: 2, angle: 90 }, objectName: name,
  });
}
function icon(slide, key, x, y, d, fill, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill || C.accent1 }, line: { type: "none" }, objectName: (name || key) + "-circulo" });
  const p = d * 0.26;
  slide.addImage({ data: ICONS[key], x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: (name || key) + "-icono", altText: key });
}
function source(slide, text) {
  txt(slide, text, { x: MX, y: 6.6, w: CW, h: 0.32, fontSize: 10, color: C.accent6, italic: true, objectName: "fuentes", valign: "bottom" });
}
function codeBox(slide, x, y, w, h, title, code, tone, name) {
  card(slide, x, y, w, h, tone === "bad" ? "F7E9E5" : "E6F2EC", name);
  txt(slide, title, { x: x + 0.25, y: y + 0.18, w: w - 0.5, h: 0.35, fontSize: 14, bold: true, color: tone === "bad" ? C.accent3 : C.accent1, objectName: name + "-titulo" });
  txt(slide, code, { x: x + 0.25, y: y + 0.6, w: w - 0.5, h: h - 0.75, fontSize: 13, fontFace: "Courier New", color: C.text1, objectName: name + "-codigo" });
}
function contentSlide(section, title) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
}
function threeCards(s, items, prefix) {
  items.forEach(([h, b], i) => {
    const x = MX + i * 4.15, y = 4.65;
    card(s, x, y, 3.85, 1.8, i === 2 ? "E6F2EC" : "FFFFFF", prefix + "-" + i);
    txt(s, h, { x: x + 0.25, y: y + 0.18, w: 3.35, h: 0.35, fontSize: 16, bold: true, color: i === 2 ? C.accent1 : C.text2, objectName: prefix + "-titulo-" + i });
    txt(s, b, { x: x + 0.25, y: y + 0.6, w: 3.35, h: 1.1, fontSize: 14, objectName: prefix + "-texto-" + i });
  });
}
function ruleCard(s, rows, name) {
  card(s, MX, 1.45, 4.6, 2.95, C.background2, name);
  txt(s, rows.flatMap(([k, v], i) => [
    { text: k, options: { bold: true, color: C.accent1, fontSize: 13, breakLine: true } },
    { text: v, options: { breakLine: i < rows.length - 1, paraSpaceAfter: 6 } },
  ]), { x: MX + 0.3, y: 1.65, w: 4.0, h: 2.65, fontSize: 14, objectName: name + "-datos" });
}
function shotCard(slide, img, ratio, lines, name) {
  const w = 4.6, h = w * ratio;
  slide.addImage({ path: __dirname + "/img/" + img, x: MX, y: 1.45, w, h, objectName: name + "-captura", altText: "Captura de SonarQube" });
  slide.addShape(pres.shapes.RECTANGLE, { x: MX, y: 1.45, w, h, fill: { type: "none" }, line: { color: "D5E3DC", width: 0.75 }, objectName: name + "-borde" });
  txt(slide, lines.map((l, i) => ({ text: l, options: { breakLine: i < lines.length - 1, bold: i === 0, color: i === 0 ? C.accent1 : C.text1 } })), { x: MX, y: 1.45 + h + 0.12, w, h: 0.75, fontSize: 12, objectName: name + "-pie" });
}
const TH = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 } } });
const TABLE = { color: C.text1, border: { type: "solid", pt: 0.75, color: "D5E3DC" }, fill: { color: C.background1 }, valign: "middle" };

async function build() {
  await loadIcons();

  // ===================== 1. Portada =====================
  pres.addSection({ title: "Presentación" });
  let s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Presentación" });
  txt(s, "DESARROLLO SEGURO · UNIDAD 2", { x: MX, y: 1.5, w: 8.4, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 2, objectName: "kicker" });
  s.addText("Revisión de seguridad del CRUD Supermercado", { placeholder: "title" });
  s.addText("Análisis con SonarQube, validación de datos en el servidor y recomendaciones para producción", { placeholder: "body" });
  txt(s, [
    { text: "Xavier Romero · Alejandro Figueroa", options: { bold: true, breakLine: true } },
    { text: "22 de octubre de 2026 · actividaddjango1.pythonanywhere.com" },
  ], { x: MX, y: 5.6, w: 8.4, h: 0.8, fontSize: 16, color: C.background1, objectName: "autores" });
  s.addShape(pres.shapes.OVAL, { x: 9.55, y: 2.0, w: 3.2, h: 3.2, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "escudo-circulo" });
  s.addImage({ data: ICONS.shield, x: 10.35, y: 2.8, w: 1.6, h: 1.6, objectName: "escudo-icono", altText: "Escudo" });
  s.addNotes(notas());

  // ===================== 2. Contexto =====================
  pres.addSection({ title: "Análisis del código" });
  s = contentSlide("Análisis del código", "Qué revisamos y cómo lo hicimos");
  [["cart", "El CRUD", "Aplicación web en Django para crear listas de compras y agregarles productos. Cada usuario ve solo sus propias listas."],
   ["form", "Operación elegida", "Agregar y editar un producto de una lista (formulario ShoppingItemForm). Revisamos dos datos: cantidad y precio unitario."],
   ["scope", "Alcance", "Ética, proceso de desarrollo seguro y validación de datos. Probamos en una copia local, con datos ficticios."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 1.45, w = 3.85, hh = 2.85;
    card(s, x, y, w, hh, C.background2, "tarjeta-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.75, C.accent1, "icono-" + i);
    txt(s, h, { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: "tarjeta-titulo-" + i });
    txt(s, b, { x: x + 0.3, y: y + 1.65, w: w - 0.6, h: 1.1, fontSize: 14, objectName: "tarjeta-texto-" + i });
  });
  [["Xavier Romero", "Análisis del código · OWASP · validación · pruebas · ISO/IEC 27034"], ["Alejandro Figueroa", "Dependencias · publicación · PythonAnywhere · ética"]].forEach(([n, r], i) => {
    const x = MX + i * 6.2, y = 4.65;
    card(s, x, y, 5.9, 1.05, "FFFFFF", "equipo-" + i);
    icon(s, "user", x + 0.25, y + 0.2, 0.65, i ? C.accent4 : C.accent1, "persona-" + i);
    txt(s, [{ text: n, options: { bold: true, breakLine: true, fontSize: 16, color: C.text2 } }, { text: r, options: { fontSize: 14 } }], { x: x + 1.1, y: y + 0.18, w: 4.6, h: 0.75, objectName: "equipo-texto-" + i });
  });
  txt(s, "Fuera de alcance: sesiones y cookies, protección de datos por industria y análisis de amenazas en profundidad (siguiente parte de la unidad).", { x: MX, y: 5.95, w: CW, h: 0.5, fontSize: 14, italic: true, color: C.accent6, objectName: "fuera-alcance" });
  s.addNotes(notas());

  // ===================== 3. SonarQube resumen =====================
  s = contentSlide("Análisis del código", "SonarQube: lo que midió y lo que no");
  card(s, MX, 1.45, 5.0, 4.15, C.background2, "ficha");
  txt(s, "Ficha del análisis", { x: MX + 0.3, y: 1.65, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: "ficha-titulo" });
  const ficha = [
    ["Herramienta", "SonarQube Community Build 26.9.0.129388 · Scanner CLI 8.0.1"],
    ["Revisión inicial", "15-10-2026 · versión publicada"],
    ["Revisión final", "20-10-2026 · versión con las correcciones"],
    ["Alcance", "37 archivos y 1.963 líneas de código propio (Python, HTML, JS y CSS)"],
    ["Exclusiones técnicas", "Solo lo que no es nuestro: entorno virtual (venv), librerías (node_modules) y archivos generados"],
  ];
  txt(s, ficha.flatMap(([k, v], i) => [
    { text: k, options: { bold: true, color: C.accent1, breakLine: true, fontSize: 13 } },
    { text: v, options: { breakLine: i < ficha.length - 1, fontSize: 14, paraSpaceAfter: 6 } },
  ]), { x: MX + 0.3, y: 2.15, w: 4.4, h: 3.35, objectName: "ficha-datos" });
  const RW = 6.78, RH = RW * 428 / 1120;
  s.addImage({ path: __dirname + "/img/sonar_resumen.png", x: 5.95, y: 1.45, w: RW, h: RH, objectName: "captura-resumen", altText: "Captura del panel de SonarQube" });
  txt(s, "Captura de SonarQube, revisión final (20-10-2026). Abajo: valor inicial → final.", { x: 5.95, y: 1.45 + RH + 0.06, w: RW, h: 0.25, fontSize: 10, italic: true, color: C.accent6, objectName: "captura-resumen-pie" });
  [["Bugs", "4 → 0"], ["Code smells", "11 → 6"], ["Cobertura", "0* → 64,7 %"]].forEach(([lbl, v], i) => {
    const x = 5.95 + i * 2.31, y = 4.5, w = 2.16, h = 1.1;
    card(s, x, y, w, h, "FFFFFF", "metrica-" + i);
    txt(s, lbl, { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: 0.3, fontSize: 11, bold: true, color: C.accent6, objectName: "metrica-label-" + i });
    txt(s, v, { x: x + 0.15, y: y + 0.45, w: w - 0.3, h: 0.55, fontSize: 20, bold: true, color: C.accent1, valign: "middle", objectName: "metrica-valor-" + i });
  });
  card(s, MX, 5.8, CW, 0.75, "FBF1E2", "limites");
  icon(s, "warn", MX + 0.2, 5.9, 0.55, C.accent2, "limites");
  txt(s, "Ojo: aprobar no es lo mismo que ser seguro. SonarQube no detectó la clave secreta débil (SECRET_KEY) ni que la cantidad aceptaba 0; lo encontramos revisando a mano. *La cobertura inicial era 0 % porque no habíamos cargado el informe, no porque faltaran pruebas.", { x: MX + 0.95, y: 5.86, w: CW - 1.15, h: 0.65, fontSize: 13, valign: "middle", objectName: "limites-texto" });
  s.addNotes(notas());

  // ===================== 4. Observación 1 =====================
  s = contentSlide("Análisis del código", "Observación 1: una búsqueda de texto que podía volverse lenta");
  shotCard(s, "sonar_s8786.png", 414 / 915, ["javascript:S8786 · Major (Reliability: Medium)", "Code Smell · calculator.js:14 · origen: SonarQube"], "ficha1");
  codeBox(s, 5.45, 1.45, 7.28, 1.35, "Antes", ".toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, \".\")", "bad", "antes1");
  codeBox(s, 5.45, 3.05, 7.28, 1.35, "Después · 19-10-2026", "new Intl.NumberFormat('es-CL').format(Math.round(amount))", "good", "despues1");
  threeCards(s, [["Qué ocurre", "Para mostrar el subtotal con puntos de miles ($12.990) se usaba un patrón de texto (regex) que, con textos muy largos, puede tardar demasiado."],
    ["Consecuencia real", "Baja: aquí solo recibe números cortos y corre en el navegador del propio usuario. Es un tema de calidad, no de seguridad."],
    ["Decisión: corregir", "Usamos el formato de números para Chile que ya trae el navegador. Muestra lo mismo: lo comprobamos con 6 montos."]], "obs1");
  s.addNotes(notas());

  // ===================== 5. Observación 2 =====================
  s = contentSlide("Análisis del código", "Observación 2: un texto repetido que escondía un riesgo");
  shotCard(s, "sonar_s1192.png", 414 / 915, ["python:S1192 · Critical (Maintainability: High)", "Code Smell · settings.py:38 · SonarQube + revisión manual"], "ficha2");
  txt(s, "¿La aplicación acepta este dominio? (configuración real, clave ficticia)", { x: 5.45, y: 1.45, w: 7.28, h: 0.35, fontSize: 14, bold: true, color: C.text2, objectName: "hosts-titulo" });
  s.addTable([
    [TH("Host"), TH("Antes"), TH("Después")],
    ["actividaddjango1.pythonanywhere.com", { text: "Sí", options: { color: C.accent1, bold: true } }, { text: "Sí, con el .env corregido", options: { color: C.accent1, bold: true } }],
    ["otro-usuario.pythonanywhere.com", { text: "Sí", options: { color: C.accent3, bold: true } }, { text: "No", options: { color: C.accent1, bold: true } }],
    ["evil.example.com", "No", "No"],
  ], Object.assign({ x: 5.45, y: 1.9, w: 7.28, colW: [3.7, 1.2, 2.38], fontSize: 13, rowH: 0.48, objectName: "tabla-hosts" }, TABLE));
  txt(s, "Evidencia: evidencia/configuracion/01_antes_hosts.txt y 03_despues_hosts_env_recomendado.txt", { x: 5.45, y: 3.95, w: 7.28, h: 0.35, fontSize: 11, italic: true, color: C.accent6, objectName: "hosts-evidencia" });
  threeCards(s, [["Qué ocurre", "Se aceptaba cualquier dominio terminado en .pythonanywhere.com (comodín), no solo el nuestro."],
    ["Consecuencia", "La app confiaba en sitios de otros usuarios y eso escondía dos errores: faltaba nuestro dominio y había un error de tipeo («ActividadDango1»)."],
    ["Decisión: corregir", "Desde el 19-10-2026 solo se aceptan los dominios declarados, y la app no arranca sin una clave secreta."]], "obs2");
  s.addNotes(notas());

  // ===================== 6. OWASP =====================
  s = contentSlide("Análisis del código", "Dos relaciones fundamentadas con OWASP Top 10:2025");
  [["A02:2025", "Security Misconfiguration", "server", C.accent4, [
      "El comodín que aceptaba dominios de otros usuarios (observación 2).",
      "La clave secreta de producción era débil (aviso W009 de Django) e igual a la de un archivo de ejemplo guardado en el repositorio (revisión manual).",
    ], "El problema está en cómo se configuró la publicación, no en la lógica de la aplicación."],
   ["A06:2025", "Insecure Design", "list", C.accent2, [
      "No existía una regla para la cantidad: el servidor aceptaba 0 y 999.999.999.",
      "El mínimo solo estaba en la página (HTML, min=1), y cualquiera se lo puede saltar.",
    ], "Faltaba el control porque faltaba la regla: primero la definimos y después la aplicamos."]].forEach(([code, name, ic, col, items, why], i) => {
    const x = MX + i * 6.2, y = 1.45, w = 5.9, h = 4.25;
    card(s, x, y, w, h, C.background2, "owasp-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.8, col, "owasp-icono-" + i);
    txt(s, [{ text: code, options: { bold: true, fontSize: 24, color: C.text2, breakLine: true } }, { text: name, options: { fontSize: 16, color: C.accent6 } }], { x: x + 1.3, y: y + 0.28, w: w - 1.6, h: 0.9, objectName: "owasp-titulo-" + i });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1, paraSpaceAfter: 8 } })), { x: x + 0.3, y: y + 1.45, w: w - 0.6, h: 1.85, fontSize: 14, objectName: "owasp-evidencia-" + i });
    txt(s, [{ text: "Por qué esta categoría: ", options: { bold: true, color: C.accent1 } }, { text: why }], { x: x + 0.3, y: y + 3.35, w: w - 0.6, h: 0.75, fontSize: 14, objectName: "owasp-porque-" + i });
  });
  txt(s, "No usamos A05 Inyección: la app consulta la base de datos con el ORM de Django, sin SQL armado a mano, y un dato fuera de rango no prueba una inyección.", { x: MX, y: 5.9, w: CW, h: 0.5, fontSize: 14, italic: true, color: C.accent6, objectName: "nota-a05" });
  source(s, "Fuentes: top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ · top10.owasp.org/2025/A06_2025-Insecure_Design/ (consultado 19-10-2026)");
  s.addNotes(notas());

  // ===================== 7. Reglas =====================
  pres.addSection({ title: "Validación y evidencia" });
  s = contentSlide("Validación y evidencia", "Reglas de los dos datos: cantidad y precio unitario");
  const rule = (t) => ({ text: t, options: { bold: true, color: C.text2, fill: { color: C.background2 } } });
  s.addTable([
    [TH("Regla"), TH("Cantidad (quantity)"), TH("Precio unitario (unit_price)")],
    [rule("Obligatoriedad"), "Obligatoria", "Opcional"],
    [rule("Tipo"), "Número entero", "Número entero, en CLP"],
    [rule("Rango o valores permitidos"), "De 1 a 999, ambos incluidos", "Mayor o igual a 0; vacío o 0 se registra como «Sin precio»"],
    [rule("Se rechaza"), "Vacío, 0, 1000, decimales", "Negativos y texto no numérico"],
    [rule("Dónde se valida"), { text: "Validadores del modelo (control nuevo)", options: { bold: true, color: C.accent1 } }, "PositiveIntegerField + ShoppingItemForm.clean() (control existente)"],
  ], Object.assign({ x: MX, y: 1.45, w: CW, colW: [2.8, 3.55, 5.78], fontSize: 14, rowH: 0.5, objectName: "tabla-reglas" }, TABLE));
  [["globe", "Página web", "Los límites del HTML (min y max) solo ayudan al usuario; se pueden saltar"],
   ["clip", "Servidor", "is_valid() revisa las reglas del modelo antes de aceptar el dato (shopping/models.py:163)"],
   ["db", "Guardado", "Solo guarda si el dato es válido; si no, muestra el error (shopping/views.py:324 y 335)"]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 4.95;
    card(s, x, y, 3.65, 1.4, i ? "FFFFFF" : "F7E9E5", "flujo-" + i);
    icon(s, ic, x + 0.2, y + 0.25, 0.6, i ? C.accent1 : C.accent3, "flujo-icono-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.95, y: y + 0.2, w: 2.55, h: 1.1, objectName: "flujo-texto-" + i });
    if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 3.72, y: y + 0.5, w: 0.36, h: 0.4, fill: { color: C.accent6 }, line: { type: "none" }, objectName: "flecha-" + i });
  });
  s.addNotes(notas());

  // ===================== 8. Mejora =====================
  s = contentSlide("Validación y evidencia", "La mejora: antes y después del control");
  codeBox(s, MX, 1.45, 5.0, 2.65, "Antes · versión publicada (15-10-2026)", "quantity = models.PositiveIntegerField(\n    default=1,\n    verbose_name='Cantidad'\n)", "bad", "antes2");
  codeBox(s, 5.85, 1.45, 6.88, 2.65, "Después · 19-10-2026", "quantity = models.PositiveIntegerField(\n    default=1,\n    validators=[\n        MinValueValidator(QUANTITY_MIN, ...),  # 1\n        MaxValueValidator(QUANTITY_MAX, ...),  # 999\n    ],\n    verbose_name='Cantidad'\n)", "good", "despues2");
  txt(s, [{ text: "Por qué: ", options: { bold: true, color: C.accent3 } }, { text: "el campo original (PositiveIntegerField) aceptaba 0 y no tenía máximo; el mínimo solo estaba en la página." }], { x: MX, y: 4.25, w: CW, h: 0.4, fontSize: 14, objectName: "motivo" });
  [["box", "Aplica en todo el CRUD", "La regla vive en el modelo: se cumple al crear, al editar y desde el panel de administración."],
   ["db", "Sin riesgo para los datos", "No cambia la base de datos. En producción, ninguno de los 15 productos estaba fuera de rango."],
   ["bullhorn", "Error claro al usuario", "Si el dato es inválido, el usuario ve qué campo falló y por qué."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 4.85;
    card(s, x, y, 3.85, 1.6, C.background2, "efecto-" + i);
    icon(s, ic, x + 0.2, y + 0.25, 0.6, C.accent1, "efecto-icono-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.95, y: y + 0.2, w: 2.75, h: 1.3, objectName: "efecto-texto-" + i });
  });
  s.addNotes(notas());

  // ===================== 9. Casos =====================
  s = contentSlide("Validación y evidencia", "Casos ejecutados: resultado antes y después");
  const ok = (t) => ({ text: t, options: { color: C.accent1, bold: true } });
  const bad = (t) => ({ text: t, options: { color: C.accent3, bold: true } });
  s.addTable([
    [TH("Campo"), TH("Dato usado"), TH("Esperado"), TH("Antes"), TH("Después")],
    ["Cantidad", "5 (dentro del rango)", "Aceptar", "Aceptado", ok("Aceptado")],
    ["Cantidad", "0 (bajo el mínimo)", "Rechazar", bad("Aceptado ✗"), ok("Rechazado ✓")],
    ["Cantidad", "1 y 999 (límites exactos)", "Aceptar", "Aceptado", ok("Aceptado")],
    ["Cantidad", "1000 (sobre el máximo)", "Rechazar", bad("Aceptado ✗"), ok("Rechazado ✓")],
    ["Precio", "1350 (legítimo)", "Aceptar", "Aceptado", ok("Aceptado")],
    ["Precio", "-5 y «abc» (inválidos)", "Rechazar", "Rechazado", ok("Rechazado")],
    ["Precio", "0 (frontera)", "Aceptar como «Sin precio»", "Sin precio", ok("Sin precio")],
    ["Backend", "POST crear con cantidad 0", "No guardar", bad("Guardó ✗"), ok("No guarda ✓")],
    ["Backend", "POST editar con cantidad 1000", "No modificar", bad("Modificó ✗"), ok("No modifica ✓")],
  ], Object.assign({ x: MX, y: 1.45, w: 8.75, colW: [1.25, 2.75, 2.05, 1.3, 1.4], fontSize: 13, rowH: 0.47, objectName: "tabla-casos" }, TABLE));
  [["4 de 13", "pruebas fallaban antes del control", C.accent3, "F7E9E5"],
   ["13 de 13", "pasan después de la mejora", C.accent1, "E6F2EC"],
   ["25 de 25", "suite completa en local y en réplica de producción, más prueba en vivo", C.accent4, C.background2]].forEach(([n, l, col, fill], i) => {
    const y = 1.45 + i * 1.6;
    card(s, 9.65, y, 3.08, 1.42, fill, "stat-" + i);
    txt(s, n, { x: 9.85, y: y + 0.15, w: 2.7, h: 0.65, fontSize: 30, bold: true, color: col, objectName: "stat-n-" + i });
    txt(s, l, { x: 9.85, y: y + 0.82, w: 2.7, h: 0.55, fontSize: 12, objectName: "stat-l-" + i });
  });
  source(s, "Pruebas automáticas de Django: envían los datos directo al servidor, sin pasar por el navegador. Evidencia: evidencia/tests/01 y 02, y evidencia/configuracion/08.");
  s.addNotes(notas());

  // ===================== 10. Trazabilidad =====================
  s = contentSlide("Validación y evidencia", "Trazabilidad del control e ISO/IEC 27034");
  [["list", "Regla", "Cantidad entre 1 y 999, definida primero", "19-10-2026"],
   ["flask", "Prueba", "13 casos; 4 fallan con el código original", "19-10-2026"],
   ["code", "Control", "Validadores del modelo en la cantidad", "19-10-2026"],
   ["check", "Verificación", "En local, en copia de producción y en vivo", "19 y 20-10-2026"],
   ["file", "Evidencia", "Resultados de pruebas, capturas y SonarQube", "carpeta evidencia"]].forEach(([ic, h, b, d], i) => {
    const x = MX + i * 2.47, y = 1.45, w = 2.2;
    icon(s, ic, x + 0.7, y, 0.8, C.accent1, "cadena-icono-" + i);
    if (i < 4) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 1.82, y: y + 0.22, w: 0.4, h: 0.36, fill: { color: C.accent5 }, line: { type: "none" }, objectName: "cadena-flecha-" + i });
    txt(s, h, { x, y: y + 0.95, w, h: 0.35, fontSize: 16, bold: true, color: C.text2, align: "center", objectName: "cadena-titulo-" + i });
    txt(s, b, { x, y: y + 1.32, w, h: 0.7, fontSize: 13, align: "center", objectName: "cadena-texto-" + i });
    txt(s, d, { x, y: y + 2.02, w, h: 0.3, fontSize: 11, color: C.accent6, align: "center", objectName: "cadena-fecha-" + i });
  });
  [["ONF", "Marco de la organización", "Las reglas generales que adoptamos: la pauta del curso, OWASP y la guía de Django."],
   ["ANF", "Marco de esta aplicación", "Las reglas de entrada propias de esta app y los controles que las cumplen."],
   ["ASC", "Control de seguridad", "El validador, junto con la prueba que demuestra que funciona."],
   ["ASMP", "Proceso de gestión", "Definir la regla, evaluar el riesgo, aplicar el control, verificarlo y dejar evidencia."]].forEach(([k, h, b], i) => {
    const x = MX + i * 3.1, y = 4.15, w = 2.85;
    card(s, x, y, w, 2.0, C.background2, "iso-" + i);
    txt(s, [{ text: k, options: { bold: true, fontSize: 20, color: C.accent1, breakLine: true } }, { text: h, options: { bold: true, fontSize: 13, color: C.text2 } }], { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, objectName: "iso-titulo-" + i });
    txt(s, b, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.95, fontSize: 13, objectName: "iso-texto-" + i });
  });
  source(s, "Aplicamos el enfoque de ISO/IEC 27034-1:2011 (confirmada en 2022); no implica certificación. Fuente: iso.org/standard/44378.html (consultado 19-10-2026)");
  s.addNotes(notas());

  // ===================== 11. Dependencias =====================
  pres.addSection({ title: "Dependencias y despliegue" });
  s = contentSlide("Dependencias y despliegue", "Python y dependencias: local frente a producción");
  card(s, MX, 1.45, CW, 0.8, C.background2, "python");
  icon(s, "cube", MX + 0.2, 1.55, 0.6, C.accent4, "python");
  txt(s, [{ text: "Python  ", options: { bold: true, color: C.text2, fontSize: 16 } }, { text: "PythonAnywhere 3.12.8 · Local 3.14.7. La versión 3.12 recibe parches de seguridad hasta 10-2028; ya existe la 3.12.15 (30-09-2026)." }], { x: MX + 1.0, y: 1.5, w: CW - 1.2, h: 0.7, fontSize: 14, valign: "middle", objectName: "python-texto" });
  const rec = (t) => ({ text: t, options: { bold: true, color: C.accent1 } });
  s.addTable([
    [TH("Dependencia"), TH("PythonAnywhere"), TH("Local"), TH("Situación consultada"), TH("Decisión")],
    [{ text: "Django", options: { bold: true } }, "6.1.1 → 6.1.2", "5.2.17 → 6.1.2", "La 6.1.2 (06-10-2026) corrige 4 fallas de seguridad (CVE); la serie 6.1 tiene soporte hasta 12-2027", rec("Actualizado en ambos entornos el 20-10; 25/25 pruebas OK")],
    [{ text: "django-environ", options: { bold: true } }, "0.14.0", "0.14.0", "Es la última versión (18-06-2026), sin avisos de seguridad (GitHub y OSV); aún no declara soporte oficial para Django 6.1", rec("Mantener (fijada); vigilar el soporte declarado de 6.1")],
    [{ text: "django-tailwind", options: { bold: true } }, "4.5.0", "4.2.0 → 4.5.0", "La lista de dependencias pedía 4.2.0, pero producción tenía 4.5.0; la 4.6.0 trae cambios que rompen compatibilidad", rec("Fijada 4.5.0 en ambos entornos; 4.6.0 se evalúa aparte")],
  ], Object.assign({ x: MX, y: 2.45, w: CW, colW: [1.75, 1.75, 1.55, 3.9, 3.18], fontSize: 13, rowH: [0.45, 0.8, 0.8, 0.8], objectName: "tabla-dependencias" }, TABLE));
  card(s, MX, 5.55, CW, 0.9, "FBF1E2", "a03");
  icon(s, "link", MX + 0.2, 5.67, 0.6, C.accent2, "a03");
  txt(s, "La lista de dependencias aceptaba cualquier versión nueva («Django>=5.0.0»), por eso local y producción quedaron distintos: riesgo de cadena de suministro (A03:2025). Ahora requirements.txt fija versiones exactas; pip check no muestra conflictos.", { x: MX + 1.0, y: 5.6, w: CW - 1.2, h: 0.8, fontSize: 14, valign: "middle", objectName: "a03-texto" });
  source(s, "Fuentes: djangoproject.com/download y /weblog/2026/oct/06 · devguide.python.org/versions · PyPI django-environ y django-tailwind (consultado 19-10-2026)");
  s.addNotes(notas());

  // ===================== 12. Recomendaciones =====================
  s = contentSlide("Dependencias y despliegue", "Dos recomendaciones priorizadas para PythonAnywhere");
  [["DEBUG=False", "Correcto en producción", C.accent1, "check"], ["ALLOWED_HOSTS", "Sin el dominio real", C.accent3, "xmark"], ["SECRET_KEY", "Débil y versionada", C.accent3, "xmark"]].forEach(([k, v, col, ic], i) => {
    const x = MX + i * 4.15;
    card(s, x, 1.45, 3.85, 0.85, "FFFFFF", "estado-" + i);
    icon(s, ic, x + 0.2, 1.57, 0.6, col, "estado-icono-" + i);
    txt(s, [{ text: k, options: { bold: true, fontSize: 15, color: C.text2, breakLine: true } }, { text: v, options: { fontSize: 13 } }], { x: x + 0.95, y: 1.52, w: 2.75, h: 0.7, valign: "middle", objectName: "estado-texto-" + i });
  });
  txt(s, "Estado observado el 19-10", { x: MX, y: 2.32, w: 4, h: 0.25, fontSize: 10, italic: true, color: C.accent6, objectName: "estado-nota" });
  [["1", "Rotar la SECRET_KEY", "key", [
      ["Evidencia: ", "Django la marcaba como débil (aviso W009 de check --deploy) y era la misma del archivo de ejemplo guardado en el repositorio. La comparamos sin mostrarla."],
      ["Acción: ", "generar una clave nueva y guardarla solo en el servidor (.env). Efecto: los usuarios deben volver a iniciar sesión."],
      ["Estado: ", "aplicada el 20-10-2026; el aviso ya no aparece."]]],
   ["2", "Declarar el dominio exacto", "globe", [
      ["Evidencia: ", "la configuración no incluía nuestro dominio y tenía un error de tipeo («ActividadDango1»); funcionaba solo gracias al comodín."],
      ["Acción: ", "declarar solo actividaddjango1.pythonanywhere.com (ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS) antes de publicar el código nuevo; si no, el sitio se cae."],
      ["Estado: ", "aplicada el 20-10-2026, con HTTPS obligatorio; inicio de sesión verificado."]]]].forEach(([n, h, ic, rows], i) => {
    const x = MX + i * 6.2, y = 2.65, w = 5.9, hh = 3.85;
    card(s, x, y, w, hh, C.background2, "reco-" + i);
    icon(s, ic, x + 0.3, y + 0.25, 0.7, i ? C.accent2 : C.accent3, "reco-icono-" + i);
    txt(s, [{ text: "Prioridad " + n, options: { fontSize: 13, bold: true, color: C.accent6, breakLine: true } }, { text: h, options: { fontSize: 20, bold: true, color: C.text2 } }], { x: x + 1.2, y: y + 0.22, w: w - 1.45, h: 0.8, objectName: "reco-titulo-" + i });
    txt(s, rows.flatMap(([a, b], j) => [{ text: a, options: { bold: true, color: j === 2 ? C.accent1 : C.text2 } }, { text: b, options: { breakLine: j < rows.length - 1, paraSpaceAfter: 8 } }]), { x: x + 0.3, y: y + 1.15, w: w - 0.6, h: 2.6, fontSize: 14, objectName: "reco-texto-" + i });
  });
  source(s, "Fuente: docs.djangoproject.com/en/6.1/howto/deployment/checklist/ (consultado 19-10-2026). Evidencia: evidencia/configuracion/00 a 08. Ningún secreto aparece en láminas ni evidencias.");
  s.addNotes(notas());

  // ===================== 13. Limitación PA =====================
  s = contentSlide("Dependencias y despliegue", "Limitación del plan gratuito: la app vence en un mes");
  card(s, MX, 1.45, 4.3, 4.95, C.text2, "vence");
  icon(s, "clock", MX + 0.35, 1.8, 0.85, C.accent2, "vence");
  txt(s, "1 mes", { x: MX + 0.35, y: 2.9, w: 3.6, h: 1.0, fontSize: 60, bold: true, color: C.background1, objectName: "vence-n" });
  txt(s, "de vigencia para la web app en cuentas gratuitas. Se renueva con el botón «Run until 1 month from today» de la pestaña Web.", { x: MX + 0.35, y: 4.05, w: 3.6, h: 1.6, fontSize: 15, color: C.background1, objectName: "vence-texto" });
  [["Cómo afecta al CRUD", "Nuestra cuenta se creó cerca del 28-09-2026. Si nadie la renueva, PythonAnywhere deshabilita el sitio y el CRUD deja de estar disponible, aunque el código esté bien."],
   ["Cuenta posterior al 15-01-2026", "No incluye MySQL ni tareas programadas: la app usa SQLite y la librería de MySQL (PyMySQL) queda sin uso."],
   ["Otros límites del plan", "100 segundos de CPU al día, 512 MiB de disco e internet saliente solo hacia una lista de sitios permitidos."],
   ["Mitigación aplicada", "Vencía el 24-10-2026; la renovamos el 20-10 y ahora vence el 21-11-2026. Hay que renovarla cada mes y respaldar db.sqlite3."]].forEach(([h, b], i) => {
    const y = 1.45 + i * 1.27;
    card(s, 5.2, y, 7.53, 1.12, i === 3 ? "E6F2EC" : C.background2, "efecto-pa-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: i === 3 ? C.accent1 : C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: 5.45, y: y + 0.12, w: 7.1, h: 0.92, objectName: "efecto-pa-texto-" + i });
  });
  source(s, "Es una restricción del plan, no una falla de seguridad. Fuentes: help.pythonanywhere.com/pages/FreeAccountsFeatures/ · blog.pythonanywhere.com/221/ (consultado 19-10-2026)");
  s.addNotes(notas());

  // ===================== 14. Ética =====================
  pres.addSection({ title: "Ética y cierre" });
  s = contentSlide("Ética y cierre", "Ética: lo que hicimos y lo que no haríamos");
  [["Acciones éticas", C.accent1, "check", ["Publicar los hallazgos reales, incluidos los nuestros: solo excluimos carpetas técnicas de SonarQube.", "Tratar el secreto como secreto: comparamos la SECRET_KEY por hash; no aparece en láminas ni evidencias."]],
   ["Acciones no éticas", C.accent3, "xmark", ["Excluir código de la app o inventar resultados para aprobar el Quality Gate.", "Probar contra la app de otro usuario de PythonAnywhere o usar datos reales de personas."]]].forEach(([h, col, ic, items], i) => {
    const x = MX + i * 4.15, y = 1.45, w = 3.85, hh = 3.15;
    card(s, x, y, w, hh, i ? "F7E9E5" : "E6F2EC", "etica-" + i);
    icon(s, ic, x + 0.25, y + 0.25, 0.6, col, "etica-icono-" + i);
    txt(s, h, { x: x + 1.0, y: y + 0.3, w: w - 1.2, h: 0.5, fontSize: 17, bold: true, color: col, valign: "middle", objectName: "etica-titulo-" + i });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1, paraSpaceAfter: 8 } })), { x: x + 0.25, y: y + 1.0, w: w - 0.5, h: 2.05, fontSize: 14, objectName: "etica-items-" + i });
  });
  card(s, 8.9, 1.45, 3.83, 3.15, C.background2, "decision");
  icon(s, "scale", 9.15, 1.7, 0.6, C.accent4, "decision");
  txt(s, "Nuestra decisión", { x: 9.9, y: 1.75, w: 2.7, h: 0.5, fontSize: 17, bold: true, color: C.text2, valign: "middle", objectName: "decision-titulo" });
  txt(s, "Probamos en una copia local, con datos ficticios, y mostramos el resultado completo aunque revele errores propios. Ocultarlos protegería la nota, no a los usuarios.", { x: 9.15, y: 2.5, w: 3.35, h: 2.0, fontSize: 14, objectName: "decision-texto" });
  card(s, MX, 4.85, CW, 1.6, C.text2, "concientizacion");
  icon(s, "bullhorn", MX + 0.3, 5.2, 0.85, C.accent2, "concientizacion");
  txt(s, [
    { text: "Acción de concientización: «Checklist de 5 minutos antes del push»", options: { bold: true, fontSize: 17, color: C.background1, breakLine: true } },
    { text: "Afiche en el README del repositorio y charla de 10 minutos al curso en la próxima clase. Antes de cada push: 1) revisar que el diff no tenga secretos; 2) ejecutar check --deploy; 3) pruebas en verde; 4) .env fuera de git.", options: { fontSize: 14, color: C.background1 } },
  ], { x: MX + 1.45, y: 5.0, w: CW - 1.7, h: 1.35, valign: "middle", objectName: "concientizacion-texto" });
  s.addNotes(notas());

  // ===================== 15. Conclusión =====================
  s = pres.addSlide({ masterName: "CIERRE", sectionTitle: "Ética y cierre" });
  txt(s, "CONCLUSIÓN DEL EQUIPO", { x: MX, y: 0.7, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 2, objectName: "kicker-conclusion" });
  s.addText("La herramienta orienta; la revisión y la evidencia deciden", { placeholder: "title" });
  [["gauge", "Aprobar no basta", "Los tres problemas más serios (clave débil, cantidad sin límite y error de configuración) los encontramos revisando a mano."],
   ["clip", "Un control se demuestra", "Regla → prueba → control → evidencia, cada paso con su fecha."],
   ["lightbulb", "Aplicado en producción", "Clave nueva, dominio exacto, HTTPS obligatorio, Django 6.1.2 y app renovada. Pendiente: 6 alertas menores de mantenibilidad."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 2.55, w = 3.85, hh = 3.1;
    card(s, x, y, w, hh, "164A39", "cierre-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.75, C.accent1, "cierre-icono-" + i);
    txt(s, h, { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.45, fontSize: 18, bold: true, color: C.background1, objectName: "cierre-titulo-" + i });
    txt(s, b, { x: x + 0.3, y: y + 1.7, w: w - 0.6, h: 1.3, fontSize: 14, color: C.accent5, objectName: "cierre-texto-" + i });
  });
  txt(s, "Gracias · ¿Preguntas?", { x: MX, y: 6.15, w: CW, h: 0.6, fontSize: 24, bold: true, color: C.accent2, objectName: "gracias" });
  s.addNotes(notas());

  // ===================== 16. Anexo: fuentes =====================
  pres.addSection({ title: "Anexo" });
  s = contentSlide("Anexo", "Anexo: fuentes consultadas el 19-10-2026");
  const fuentes = [
    ["OWASP Top 10:2025", "https://top10.owasp.org/2025/"],
    ["ISO/IEC 27034-1:2011", "https://www.iso.org/standard/44378.html"],
    ["Django: validación de formularios", "https://docs.djangoproject.com/en/6.1/ref/forms/validation/"],
    ["Django: validadores", "https://docs.djangoproject.com/en/6.1/ref/validators/"],
    ["Django: checklist de despliegue", "https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/"],
    ["Django: versiones soportadas", "https://www.djangoproject.com/download/"],
    ["Django: security releases 06-10-2026", "https://www.djangoproject.com/weblog/2026/oct/06/security-releases/"],
    ["Python: ciclo de vida", "https://devguide.python.org/versions/"],
    ["django-environ (PyPI)", "https://pypi.org/project/django-environ/"],
    ["django-tailwind (PyPI y changelog)", "https://pypi.org/project/django-tailwind/"],
    ["PythonAnywhere: cuentas gratuitas", "https://help.pythonanywhere.com/pages/FreeAccountsFeatures/"],
    ["PythonAnywhere: cambios plan gratuito", "https://blog.pythonanywhere.com/221/"],
  ];
  const half = Math.ceil(fuentes.length / 2);
  [fuentes.slice(0, half), fuentes.slice(half)].forEach((col, i) => {
    txt(s, col.flatMap(([n, u], j) => [
      { text: n, options: { bold: true, color: C.text2, breakLine: true, fontSize: 13 } },
      { text: u, options: { hyperlink: { url: u }, color: C.accent1, fontSize: 12, breakLine: j < col.length - 1, paraSpaceAfter: 8 } },
    ]), { x: MX + i * 6.2, y: 1.45, w: 5.9, h: 5.0, objectName: "fuentes-col-" + i });
  });
  s.addNotes(notas());

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("OK", OUT);
}
build().catch((e) => { console.error(e); process.exit(1); });
