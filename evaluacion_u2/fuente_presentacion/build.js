// Generador de la presentación Evaluación U2 — Desarrollo Seguro.
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa6");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const OUT = process.argv[2] || "deck.pptx";

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
const TH = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 } } });
const TABLE = { color: C.text1, border: { type: "solid", pt: 0.75, color: "D5E3DC" }, fill: { color: C.background1 }, valign: "middle" };

async function build() {
  await loadIcons();

  // ===================== 1. Portada =====================
  pres.addSection({ title: "Presentación" });
  let s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Presentación" });
  txt(s, "DESARROLLO SEGURO · UNIDAD 2 · CRITERIOS 2.1.1 A 2.1.3", { x: MX, y: 1.5, w: 8.4, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 2, objectName: "kicker" });
  s.addText("Revisión de seguridad del CRUD Supermercado", { placeholder: "title" });
  s.addText("SonarQube, validación en el servidor y recomendaciones de despliegue", { placeholder: "body" });
  txt(s, [
    { text: "Xavier Romero · Alejandro Figueroa", options: { bold: true, breakLine: true } },
    { text: "22 de octubre de 2026 · actividaddjango1.pythonanywhere.com" },
  ], { x: MX, y: 5.6, w: 8.4, h: 0.8, fontSize: 16, color: C.background1, objectName: "autores" });
  s.addShape(pres.shapes.OVAL, { x: 9.55, y: 2.0, w: 3.2, h: 3.2, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "escudo-circulo" });
  s.addImage({ data: ICONS.shield, x: 10.35, y: 2.8, w: 1.6, h: 1.6, objectName: "escudo-icono", altText: "Escudo" });
  s.addNotes(`[XAVIER · 10 s]
Buenos días. Somos Xavier Romero y Alejandro Figueroa y presentamos la revisión de seguridad de nuestro CRUD de listas de compras, publicado en PythonAnywhere. Yo cubro el análisis y la validación; Alejandro, dependencias, despliegue y ética.`);

  // ===================== 2. Contexto =====================
  pres.addSection({ title: "Análisis del código" });
  s = contentSlide("Análisis del código", "Qué revisamos y cómo lo hicimos");
  [["cart", "El CRUD", "Listas de compras y sus productos en Django 6.1 (producción). Cada usuario ve solo sus propias listas."],
   ["form", "Operación elegida", "Agregar y editar un producto de una lista (ShoppingItemForm). Campos revisados: cantidad y precio unitario."],
   ["scope", "Alcance", "Ética, ciclo seguro y validación de entradas. Pruebas en copia local con datos ficticios, rama evaluacion-u2."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 1.45, w = 3.85, hh = 2.85;
    card(s, x, y, w, hh, C.background2, "tarjeta-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.75, C.accent1, "icono-" + i);
    txt(s, h, { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: "tarjeta-titulo-" + i });
    txt(s, b, { x: x + 0.3, y: y + 1.65, w: w - 0.6, h: 1.1, fontSize: 14, objectName: "tarjeta-texto-" + i });
  });
  [["Xavier Romero", "SonarQube · OWASP · validación · pruebas · ISO/IEC 27034"], ["Alejandro Figueroa", "Dependencias · despliegue · PythonAnywhere · ética"]].forEach(([n, r], i) => {
    const x = MX + i * 6.2, y = 4.65;
    card(s, x, y, 5.9, 1.05, "FFFFFF", "equipo-" + i);
    icon(s, "user", x + 0.25, y + 0.2, 0.65, i ? C.accent4 : C.accent1, "persona-" + i);
    txt(s, [{ text: n, options: { bold: true, breakLine: true, fontSize: 16, color: C.text2 } }, { text: r, options: { fontSize: 14 } }], { x: x + 1.1, y: y + 0.18, w: 4.6, h: 0.75, objectName: "equipo-texto-" + i });
  });
  txt(s, "Fuera de alcance: sesiones y cookies, protección de datos por industria y análisis de amenazas en profundidad (siguiente parte de la unidad).", { x: MX, y: 5.95, w: CW, h: 0.5, fontSize: 14, italic: true, color: C.accent6, objectName: "fuera-alcance" });
  s.addNotes(`[XAVIER · 25 s]
Es un CRUD de listas de compras: cada usuario crea listas y les agrega productos con cantidad y precio en pesos. Elegimos una operación, agregar y editar un producto, con dos campos de reglas distintas: la cantidad, obligatoria y con rango, y el precio, opcional y con la opción "sin precio". Trabajamos en una copia local, con datos ficticios y en una rama separada, para que cada cambio quede trazable.`);

  // ===================== 3. SonarQube resumen =====================
  s = contentSlide("Análisis del código", "SonarQube: lo que midió y lo que no");
  card(s, MX, 1.45, 5.0, 4.15, C.background2, "ficha");
  txt(s, "Ficha del análisis", { x: MX + 0.3, y: 1.65, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: C.text2, objectName: "ficha-titulo" });
  const ficha = [
    ["Herramienta", "SonarQube Community Build 26.9.0.129388 · Scanner CLI 8.0.1"],
    ["Análisis inicial", "15-10-2026 · commit 2516b9f (main)"],
    ["Análisis final", "20-10-2026 · commit 019c866 (evaluacion-u2)"],
    ["Alcance", "37 archivos · 1.963 líneas: Python, HTML, JS y CSS propios"],
    ["Exclusiones técnicas", "venv, node_modules, __pycache__, staticfiles, media, cachés y carpeta de entrega"],
  ];
  txt(s, ficha.flatMap(([k, v], i) => [
    { text: k, options: { bold: true, color: C.accent1, breakLine: true, fontSize: 13 } },
    { text: v, options: { breakLine: i < ficha.length - 1, fontSize: 14, paraSpaceAfter: 6 } },
  ]), { x: MX + 0.3, y: 2.15, w: 4.4, h: 3.35, objectName: "ficha-datos" });
  [["Quality Gate", "OK", "OK"], ["Vulnerabilidades", "0", "0"], ["Security Hotspots", "0", "0"],
   ["Bugs", "4", "0"], ["Code smells", "11", "6"], ["Cobertura", "0 %*", "64,7 %"]].forEach(([lbl, a, b], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 5.95 + col * 2.3, y = 1.45 + row * 2.1, w = 2.1, h = 1.95;
    card(s, x, y, w, h, "FFFFFF", "metrica-" + i);
    txt(s, lbl + " (final)", { x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.35, fontSize: 13, bold: true, color: C.accent6, objectName: "metrica-label-" + i });
    txt(s, b, { x: x + 0.2, y: y + 0.6, w: w - 0.4, h: 0.75, fontSize: 32, bold: true, color: C.accent1, valign: "middle", objectName: "metrica-valor-" + i });
    txt(s, "Inicial: " + a, { x: x + 0.2, y: y + 1.45, w: w - 0.4, h: 0.3, fontSize: 12, color: C.accent6, objectName: "metrica-nota-" + i });
  });
  card(s, MX, 5.8, CW, 0.75, "FBF1E2", "limites");
  icon(s, "warn", MX + 0.2, 5.9, 0.55, C.accent2, "limites");
  txt(s, "Límites: con 0 vulnerabilidades, SonarQube no detectó la SECRET_KEY débil ni la falta de rango en la cantidad; ambas salieron de revisión manual. *Cobertura 0 % inicial: el informe no estaba importado, no significa que faltaran pruebas.", { x: MX + 0.95, y: 5.86, w: CW - 1.15, h: 0.65, fontSize: 13, valign: "middle", objectName: "limites-texto" });
  s.addNotes(`[XAVIER · 40 s]
Usamos SonarQube Community Build 26.9 local. El primer análisis fue el 15 de octubre sobre main y el final el 20, sobre nuestra rama. Solo excluimos carpetas técnicas, como el entorno virtual y archivos generados; nunca código de la app.
El Quality Gate aprobó en ambos y no hubo vulnerabilidades ni hotspots. Pero eso no significa que la app sea segura: SonarQube no detectó la clave secreta débil ni que la cantidad aceptaba cero; eso salió de la revisión manual. Y el 0 % de cobertura inicial era porque no habíamos importado el informe, no porque faltaran pruebas.

Fuente (no leer): http://localhost:9000/dashboard?id=desarrollo-seguro-django · capturas en evidencia/capturas · JSON en evidencia/sonarqube`);

  // ===================== 4. Observación 1 =====================
  s = contentSlide("Análisis del código", "Observación 1: regex con backtracking en el formato CLP");
  ruleCard(s, [
    ["Regla", "javascript:S8786 · Regular expressions should not cause non-linear backtracking"],
    ["Tipo y severidad en nuestra instalación", "Code Smell · Major (Reliability: Medium)"],
    ["Archivo y origen", "static/shopping/js/calculator.js:14 · SonarQube"],
  ], "ficha1");
  codeBox(s, 5.45, 1.45, 7.28, 1.35, "Antes", ".toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, \".\")", "bad", "antes1");
  codeBox(s, 5.45, 3.05, 7.28, 1.35, "Después · commit cbab41a", "new Intl.NumberFormat('es-CL').format(Math.round(amount))", "good", "despues1");
  threeCards(s, [["Qué ocurre", "El subtotal se formatea en el navegador con una regex de búsqueda anticipada anidada."],
    ["Consecuencia real", "Baja: solo recibe dígitos de Math.round() en el navegador del propio usuario. Es calidad, no una vulnerabilidad explotable."],
    ["Decisión: corregir", "Formato nativo es-CL. Misma salida verificada con 6 montos, de $0 a $9.999.999.000."]], "obs1");
  s.addNotes(`[XAVIER · 35 s]
Primera observación: la regla S8786, una regex que puede tardar de forma no lineal por backtracking. En nuestro caso formatea el subtotal en el navegador. Revisamos el contexto: solo recibe dígitos de Math.round y corre en el navegador del propio usuario, así que es un problema de calidad, no una vulnerabilidad; SonarQube también la clasifica como code smell. Igual la corregimos porque era simple: usamos el formato nativo chileno y verificamos la misma salida con seis montos.`);

  // ===================== 5. Observación 2 =====================
  s = contentSlide("Análisis del código", "Observación 2: un literal repetido que ocultaba un comodín");
  ruleCard(s, [
    ["Regla", "python:S1192 · String literals should not be duplicated"],
    ["Tipo y severidad en nuestra instalación", "Code Smell · Critical (Maintainability: High)"],
    ["Archivo y origen", "supermarket_project/settings.py:38 · SonarQube + revisión manual"],
  ], "ficha2");
  txt(s, "¿Django acepta este host? (mismo .env de producción, clave ficticia)", { x: 5.45, y: 1.45, w: 7.28, h: 0.35, fontSize: 14, bold: true, color: C.text2, objectName: "hosts-titulo" });
  s.addTable([
    [TH("Host"), TH("Antes"), TH("Después")],
    ["actividaddjango1.pythonanywhere.com", { text: "Sí", options: { color: C.accent1, bold: true } }, { text: "Sí, con el .env corregido", options: { color: C.accent1, bold: true } }],
    ["otro-usuario.pythonanywhere.com", { text: "Sí", options: { color: C.accent3, bold: true } }, { text: "No", options: { color: C.accent1, bold: true } }],
    ["evil.example.com", "No", "No"],
  ], Object.assign({ x: 5.45, y: 1.9, w: 7.28, colW: [3.7, 1.2, 2.38], fontSize: 13, rowH: 0.48, objectName: "tabla-hosts" }, TABLE));
  txt(s, "Evidencia: evidencia/configuracion/01_antes_hosts.txt y 03_despues_hosts_env_recomendado.txt", { x: 5.45, y: 3.95, w: 7.28, h: 0.35, fontSize: 11, italic: true, color: C.accent6, objectName: "hosts-evidencia" });
  threeCards(s, [["Qué ocurre", "settings.py agregaba siempre el comodín *.pythonanywhere.com a ALLOWED_HOSTS y a los orígenes CSRF."],
    ["Consecuencia", "Confiaba en las apps de cualquier usuario de PythonAnywhere y ocultaba dos errores del .env: dominio ausente y el typo «ActividadDango1»."],
    ["Decisión: corregir", "Commit 11f11d0: solo los dominios declarados en el .env y SECRET_KEY obligatoria."]], "obs2");
  s.addNotes(`[XAVIER · 40 s]
La segunda parece menor: un literal repetido tres veces en settings.py. Pero al revisarlo vimos que el código agregaba siempre un comodín para todos los subdominios de pythonanywhere.com, en los hosts permitidos y en los orígenes CSRF. Es decir, confiaba en las apps de cualquier otro usuario.
Lo comprobamos con la configuración de producción: antes aceptaba "otro-usuario.pythonanywhere.com"; después, no. Además, el comodín ocultaba dos errores del .env: faltaba nuestro dominio y el origen CSRF tenía un typo. La alerta es de SonarQube; la conclusión de seguridad es de nuestra revisión manual.`);

  // ===================== 6. OWASP =====================
  s = contentSlide("Análisis del código", "Dos relaciones fundamentadas con OWASP Top 10:2025");
  [["A02:2025", "Security Misconfiguration", "server", C.accent4, [
      "Comodín de hosts y orígenes CSRF en settings.py (observación 2).",
      "SECRET_KEY de producción débil: Django la marcaba con W009 y era idéntica a la de .env.example, versionado desde el 24-09-2026 (revisión manual).",
    ], "Es configuración de despliegue insegura, no un error de lógica del CRUD."],
   ["A06:2025", "Insecure Design", "list", C.accent2, [
      "No existía una regla definida para la cantidad: el servidor aceptaba 0 y 999.999.999.",
      "El mínimo solo estaba en el HTML (min=1), que el usuario puede saltarse.",
    ], "Faltaba el control porque faltaba el requisito: se corrigió definiendo primero la regla."]].forEach(([code, name, ic, col, items, why], i) => {
    const x = MX + i * 6.2, y = 1.45, w = 5.9, h = 4.25;
    card(s, x, y, w, h, C.background2, "owasp-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.8, col, "owasp-icono-" + i);
    txt(s, [{ text: code, options: { bold: true, fontSize: 24, color: C.text2, breakLine: true } }, { text: name, options: { fontSize: 16, color: C.accent6 } }], { x: x + 1.3, y: y + 0.28, w: w - 1.6, h: 0.9, objectName: "owasp-titulo-" + i });
    txt(s, items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1, paraSpaceAfter: 8 } })), { x: x + 0.3, y: y + 1.45, w: w - 0.6, h: 1.85, fontSize: 14, objectName: "owasp-evidencia-" + i });
    txt(s, [{ text: "Por qué esta categoría: ", options: { bold: true, color: C.accent1 } }, { text: why }], { x: x + 0.3, y: y + 3.35, w: w - 0.6, h: 0.75, fontSize: 14, objectName: "owasp-porque-" + i });
  });
  txt(s, "No relacionamos A05 Inyección: el CRUD usa el ORM de Django sin SQL crudo, y un dato fuera de rango no demuestra una inyección.", { x: MX, y: 5.9, w: CW, h: 0.5, fontSize: 14, italic: true, color: C.accent6, objectName: "nota-a05" });
  source(s, "Fuentes: top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ · top10.owasp.org/2025/A06_2025-Insecure_Design/ (consultado 19-10-2026)");
  s.addNotes(`[XAVIER · 30 s]
Con OWASP 2025 hicimos dos relaciones. A02, configuración incorrecta: el comodín y la clave de producción, que Django marcaba como débil y que era la misma del archivo de ejemplo del repositorio; la comparamos por hash, sin mostrarla. A06, diseño inseguro: no había una regla definida para la cantidad, así que no había control. No usamos A05, inyección, porque usamos el ORM y no tenemos evidencia que la sostenga.

Fuentes (no leer): https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/ · https://top10.owasp.org/2025/A06_2025-Insecure_Design/ (consultadas 19-10-2026)`);

  // ===================== 7. Reglas =====================
  pres.addSection({ title: "Validación y evidencia" });
  s = contentSlide("Validación y evidencia", "Contrato de entrada: cantidad y precio unitario");
  const rule = (t) => ({ text: t, options: { bold: true, color: C.text2, fill: { color: C.background2 } } });
  s.addTable([
    [TH("Regla"), TH("Cantidad (quantity)"), TH("Precio unitario (unit_price)")],
    [rule("Obligatoriedad"), "Obligatoria", "Opcional"],
    [rule("Tipo"), "Número entero", "Número entero, en CLP"],
    [rule("Rango o valores permitidos"), "De 1 a 999, ambos incluidos", "Mayor o igual a 0; vacío o 0 se registra como «Sin precio»"],
    [rule("Se rechaza"), "Vacío, 0, 1000, decimales", "Negativos y texto no numérico"],
    [rule("Dónde se valida"), { text: "Validadores del modelo (control nuevo)", options: { bold: true, color: C.accent1 } }, "PositiveIntegerField + ShoppingItemForm.clean() (control existente)"],
  ], Object.assign({ x: MX, y: 1.45, w: CW, colW: [2.8, 3.55, 5.78], fontSize: 14, rowH: 0.5, objectName: "tabla-reglas" }, TABLE));
  [["globe", "Navegador", "min y max en HTML: solo comodidad, se pueden saltar"],
   ["clip", "ModelForm.is_valid()", "full_clean() ejecuta los validadores del modelo (shopping/models.py:163)"],
   ["db", "Vista", "form_valid() guarda; form_invalid() no guarda (shopping/views.py:324 y 335)"]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 4.95;
    card(s, x, y, 3.65, 1.4, i ? "FFFFFF" : "F7E9E5", "flujo-" + i);
    icon(s, ic, x + 0.2, y + 0.25, 0.6, i ? C.accent1 : C.accent3, "flujo-icono-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.95, y: y + 0.2, w: 2.55, h: 1.1, objectName: "flujo-texto-" + i });
    if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 3.72, y: y + 0.5, w: 0.36, h: 0.4, fill: { color: C.accent6 }, line: { type: "none" }, objectName: "flecha-" + i });
  });
  s.addNotes(`[XAVIER · 30 s]
Este es el contrato de entrada. La cantidad es obligatoria, entera, de 1 a 999. El precio es opcional, entero y mayor o igual a cero; vacío o cero se registra como "sin precio".
Abajo, dónde se valida: el HTML solo ayuda al usuario. La validación real ocurre en el servidor, cuando is_valid ejecuta los validadores del modelo. La vista solo guarda en form_valid; si el formulario es inválido, no guarda y muestra el error.

Fuente (no leer): https://docs.djangoproject.com/en/6.1/ref/forms/validation/`);

  // ===================== 8. Mejora =====================
  s = contentSlide("Validación y evidencia", "La mejora: antes y después del control");
  codeBox(s, MX, 1.45, 5.0, 2.65, "Antes · main (2516b9f)", "quantity = models.PositiveIntegerField(\n    default=1,\n    verbose_name='Cantidad'\n)", "bad", "antes2");
  codeBox(s, 5.85, 1.45, 6.88, 2.65, "Después · commit 1ae5774", "quantity = models.PositiveIntegerField(\n    default=1,\n    validators=[\n        MinValueValidator(QUANTITY_MIN, ...),  # 1\n        MaxValueValidator(QUANTITY_MAX, ...),  # 999\n    ],\n    verbose_name='Cantidad'\n)", "good", "despues2");
  txt(s, [{ text: "Por qué: ", options: { bold: true, color: C.accent3 } }, { text: "PositiveIntegerField acepta 0 y no tiene máximo. El min=1 solo estaba en el HTML (revisión manual)." }], { x: MX, y: 4.25, w: CW, h: 0.4, fontSize: 14, objectName: "motivo" });
  [["box", "Aplica en todo el CRUD", "Al estar en el modelo, aplica igual al crear, al editar y en el admin de Django."],
   ["db", "Sin riesgo para los datos", "La migración 0004 no cambia la base (no-op). En producción: 0 de 15 productos fuera de rango."],
   ["bullhorn", "Error claro al usuario", "La vista de agregar ahora informa el campo y el motivo, en vez de un mensaje genérico."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 4.85;
    card(s, x, y, 3.85, 1.6, C.background2, "efecto-" + i);
    icon(s, ic, x + 0.2, y + 0.25, 0.6, C.accent1, "efecto-icono-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: x + 0.95, y: y + 0.2, w: 2.75, h: 1.3, objectName: "efecto-texto-" + i });
  });
  s.addNotes(`[XAVIER · 25 s]
La mejora: antes, un PositiveIntegerField, que acepta cero y no tiene máximo. Después, dos validadores, mínimo 1 y máximo 999. Lo pusimos en el modelo para que aplique al crear, al editar y en el admin. La migración no cambia la base, y en producción ninguno de los 15 productos guardados quedaba fuera de rango.

Fuente (no leer): https://docs.djangoproject.com/en/6.1/ref/validators/`);

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
   ["13 de 13", "pasan después (commit 1ae5774)", C.accent1, "E6F2EC"],
   ["25 de 25", "suite completa en local y en réplica de producción, más prueba en vivo", C.accent4, C.background2]].forEach(([n, l, col, fill], i) => {
    const y = 1.45 + i * 1.6;
    card(s, 9.65, y, 3.08, 1.42, fill, "stat-" + i);
    txt(s, n, { x: 9.85, y: y + 0.15, w: 2.7, h: 0.65, fontSize: 30, bold: true, color: col, objectName: "stat-n-" + i });
    txt(s, l, { x: 9.85, y: y + 0.82, w: 2.7, h: 0.55, fontSize: 12, objectName: "stat-l-" + i });
  });
  source(s, "Pruebas Django (TestCase y cliente de pruebas): no pasan por el navegador. Evidencia: evidencia/tests/01 y 02, y evidencia/configuracion/08 (prueba en vivo)");
  s.addNotes(`[XAVIER · 40 s + demo 20 s]
Los casos son pruebas automáticas de Django, sin navegador. Para la cantidad: un valor normal, el cero, los límites 1 y 999, y el mil. Para el precio: un valor legítimo, un negativo, un texto y el cero. Y dos POST directos a las vistas.
Primero corrimos las pruebas contra el código original: fallaron 4 de 13, porque el servidor guardó un producto con cantidad cero. Ese es nuestro antes real. Después del control pasan las 13, y la suite completa, 25 de 25. Les muestro una.

DEMO (terminal en la raíz del proyecto, venv activo):
python manage.py test shopping.tests.ShoppingItemValidationTests.test_backend_crear_con_cantidad_cero_no_guarda -v 2
Primero aparecen líneas "Applying..." de la base de prueba; al final debe decir "... ok" y "OK". Decir: "envía cantidad 0 directo a la vista y comprueba que no se guarda nada".`);

  // ===================== 10. Trazabilidad =====================
  s = contentSlide("Validación y evidencia", "Trazabilidad del control e ISO/IEC 27034");
  [["list", "Requisito", "Regla 1–999 definida en el contrato de pruebas", "19-10 16:57 · feed220"],
   ["flask", "Prueba", "13 casos; 4 fallan con el código original", "19-10 16:57 · feed220"],
   ["code", "Control", "Validadores del modelo en quantity", "19-10 16:57 · 1ae5774"],
   ["check", "Verificación", "13/13, 25/25 y prueba en vivo en producción", "19 y 20-10"],
   ["file", "Evidencia", "Commits, salidas de pruebas, capturas y SonarQube", "evaluacion_u2/evidencia"]].forEach(([ic, h, b, d], i) => {
    const x = MX + i * 2.47, y = 1.45, w = 2.2;
    icon(s, ic, x + 0.7, y, 0.8, C.accent1, "cadena-icono-" + i);
    if (i < 4) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 1.82, y: y + 0.22, w: 0.4, h: 0.36, fill: { color: C.accent5 }, line: { type: "none" }, objectName: "cadena-flecha-" + i });
    txt(s, h, { x, y: y + 0.95, w, h: 0.35, fontSize: 16, bold: true, color: C.text2, align: "center", objectName: "cadena-titulo-" + i });
    txt(s, b, { x, y: y + 1.32, w, h: 0.7, fontSize: 13, align: "center", objectName: "cadena-texto-" + i });
    txt(s, d, { x, y: y + 2.02, w, h: 0.3, fontSize: 11, color: C.accent6, align: "center", objectName: "cadena-fecha-" + i });
  });
  [["ONF", "Marco normativo de la organización", "Aquí: la pauta del curso, OWASP y el checklist de despliegue de Django."],
   ["ANF", "Marco normativo de la aplicación", "El contrato de entradas de esta app y los controles que lo cumplen."],
   ["ASC", "Control de seguridad de la aplicación", "El validador más su medición de verificación: las pruebas."],
   ["ASMP", "Proceso de gestión", "Requisito → riesgo → control → verificación → auditoría, con evidencia."]].forEach(([k, h, b], i) => {
    const x = MX + i * 3.1, y = 4.15, w = 2.85;
    card(s, x, y, w, 2.0, C.background2, "iso-" + i);
    txt(s, [{ text: k, options: { bold: true, fontSize: 20, color: C.accent1, breakLine: true } }, { text: h, options: { bold: true, fontSize: 13, color: C.text2 } }], { x: x + 0.2, y: y + 0.15, w: w - 0.4, h: 0.75, objectName: "iso-titulo-" + i });
    txt(s, b, { x: x + 0.2, y: y + 0.95, w: w - 0.4, h: 0.95, fontSize: 13, objectName: "iso-texto-" + i });
  });
  source(s, "Aplicamos el enfoque de ISO/IEC 27034-1:2011 (confirmada en 2022); no implica certificación. Fuente: iso.org/standard/44378.html (consultado 19-10-2026)");
  s.addNotes(`[XAVIER · 35 s]
Esta es la trazabilidad: el requisito quedó definido en las pruebas, las pruebas fallaron antes del control, el control se implementó en un commit propio y se verificó en local, en una réplica de producción y en vivo. Todo con fecha y evidencia.
Con ISO 27034 lo relacionamos así: el ONF son las reglas que adoptamos; el ANF, el contrato de esta app; el ASC, el validador junto con sus pruebas; y el ASMP, este proceso que deja evidencia. Aplicamos su enfoque; no decimos que el proyecto esté certificado.

Fuente (no leer): https://www.iso.org/standard/44378.html (ISO/IEC 27034-1:2011, confirmada en 2022)`);

  // ===================== 11. Dependencias =====================
  pres.addSection({ title: "Dependencias y despliegue" });
  s = contentSlide("Dependencias y despliegue", "Python y dependencias: local frente a producción");
  card(s, MX, 1.45, CW, 0.8, C.background2, "python");
  icon(s, "cube", MX + 0.2, 1.55, 0.6, C.accent4, "python");
  txt(s, [{ text: "Python  ", options: { bold: true, color: C.text2, fontSize: 16 } }, { text: "PythonAnywhere 3.12.8 · Local 3.14.7. La serie 3.12 está en fase de seguridad hasta 10-2028; el último parche es 3.12.15, del 30-09-2026." }], { x: MX + 1.0, y: 1.5, w: CW - 1.2, h: 0.7, fontSize: 14, valign: "middle", objectName: "python-texto" });
  const rec = (t) => ({ text: t, options: { bold: true, color: C.accent1 } });
  s.addTable([
    [TH("Dependencia"), TH("PythonAnywhere"), TH("Local"), TH("Situación consultada"), TH("Decisión")],
    [{ text: "Django", options: { bold: true } }, "6.1.1 → 6.1.2", "5.2.17 → 6.1.2", "6.1.2 (06-10-2026) corrige 4 CVE; la serie 6.1 tiene soporte hasta 12-2027", rec("Actualizado en ambos entornos el 20-10; 25/25 pruebas OK")],
    [{ text: "django-environ", options: { bold: true } }, "0.14.0", "0.14.0", "Última versión (18-06-2026); sin avisos en GitHub ni OSV; declara Django hasta 6.0", rec("Mantener (fijada); vigilar el soporte declarado de 6.1")],
    [{ text: "django-tailwind", options: { bold: true } }, "4.5.0", "4.2.0 → 4.5.0", "requirements fijaba 4.2.0, pero producción tenía 4.5.0; la 4.6.0 trae cambios incompatibles", rec("Fijada 4.5.0 en ambos entornos; 4.6.0 se evalúa aparte")],
  ], Object.assign({ x: MX, y: 2.45, w: CW, colW: [1.75, 1.75, 1.55, 3.9, 3.18], fontSize: 13, rowH: [0.45, 0.8, 0.8, 0.8], objectName: "tabla-dependencias" }, TABLE));
  card(s, MX, 5.55, CW, 0.9, "FBF1E2", "a03");
  icon(s, "link", MX + 0.2, 5.67, 0.6, C.accent2, "a03");
  txt(s, "«Django>=5.0.0» permitió que local y producción usaran series distintas (A03:2025 Software Supply Chain Failures). Ahora requirements.txt fija versiones exactas (commit f29535c). pip check: sin conflictos en ambos entornos.", { x: MX + 1.0, y: 5.6, w: CW - 1.2, h: 0.8, fontSize: 14, valign: "middle", objectName: "a03-texto" });
  source(s, "Fuentes: djangoproject.com/download y /weblog/2026/oct/06 · devguide.python.org/versions · PyPI django-environ y django-tailwind (consultado 19-10-2026)");
  s.addNotes(`[ALEJANDRO · 45 s]
Revisamos Python y tres dependencias en los dos entornos. Producción usa Python 3.12, con soporte de seguridad hasta 2028.
En Django encontramos dos cosas: local y producción usaban series distintas, y producción tenía 6.1.1, cuando la 6.1.2 corrige cuatro CVE. Antes de actualizar revisamos las notas, que fuera la misma serie y que pasaran las 25 pruebas; recién ahí actualizamos ambos entornos.
django-environ está al día y sin avisos. En django-tailwind, el requirements no coincidía con producción; fijamos la 4.5.0. La causa era usar "mayor o igual" en requirements, que relacionamos con A03.

Fuentes (no leer, consultadas 19-10-2026):
https://www.djangoproject.com/download/
https://www.djangoproject.com/weblog/2026/oct/06/security-releases/
https://devguide.python.org/versions/
https://pypi.org/project/django-environ/
https://pypi.org/project/django-tailwind/`);

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
      ["Evidencia: ", "check --deploy marcaba W009 (prefijo «django-insecure-») y el mismo valor estaba en .env.example, versionado en git (comparado por hash, sin exponerlo)."],
      ["Acción: ", "clave nueva con get_random_secret_key(), solo en el .env de PythonAnywhere. Cierra las sesiones activas, algo aceptable."],
      ["Estado: ", "aplicada el 20-10; W009 ya no aparece en producción."]]],
   ["2", "Declarar el dominio exacto", "globe", [
      ["Evidencia: ", "ALLOWED_HOSTS=127.0.0.1,localhost y origen CSRF con el typo «ActividadDango1»; el sitio funcionaba solo por el comodín."],
      ["Acción: ", "ALLOWED_HOSTS y CSRF_TRUSTED_ORIGINS solo con actividaddjango1.pythonanywhere.com, antes de desplegar la rama (si no, Error 400)."],
      ["Estado: ", "aplicada el 20-10, con Force HTTPS activado; login verificado en vivo."]]]].forEach(([n, h, ic, rows], i) => {
    const x = MX + i * 6.2, y = 2.65, w = 5.9, hh = 3.85;
    card(s, x, y, w, hh, C.background2, "reco-" + i);
    icon(s, ic, x + 0.3, y + 0.25, 0.7, i ? C.accent2 : C.accent3, "reco-icono-" + i);
    txt(s, [{ text: "Prioridad " + n, options: { fontSize: 13, bold: true, color: C.accent6, breakLine: true } }, { text: h, options: { fontSize: 20, bold: true, color: C.text2 } }], { x: x + 1.2, y: y + 0.22, w: w - 1.45, h: 0.8, objectName: "reco-titulo-" + i });
    txt(s, rows.flatMap(([a, b], j) => [{ text: a, options: { bold: true, color: j === 2 ? C.accent1 : C.text2 } }, { text: b, options: { breakLine: j < rows.length - 1, paraSpaceAfter: 8 } }]), { x: x + 0.3, y: y + 1.15, w: w - 0.6, h: 2.6, fontSize: 14, objectName: "reco-texto-" + i });
  });
  source(s, "Fuente: docs.djangoproject.com/en/6.1/howto/deployment/checklist/ (consultado 19-10-2026). Evidencia: evidencia/configuracion/00 a 08. Ningún secreto aparece en láminas ni evidencias.");
  s.addNotes(`[ALEJANDRO · 40 s]
En producción, DEBUG estaba bien. Prioridad uno: rotar la clave secreta, porque Django la marcaba como débil y estaba en el repositorio. Generamos una nueva solo en el servidor; el aviso desapareció y el costo fue cerrar las sesiones abiertas.
Prioridad dos: declarar el dominio exacto. El .env no tenía nuestro dominio y el origen CSRF tenía un typo; funcionaba solo por el comodín. Por eso primero corregimos el .env y después desplegamos, o el sitio daba error 400. También activamos HTTPS forzado y verificamos el login en vivo.

Fuente (no leer): https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/`);

  // ===================== 13. Limitación PA =====================
  s = contentSlide("Dependencias y despliegue", "Limitación del plan gratuito: la app vence en un mes");
  card(s, MX, 1.45, 4.3, 4.95, C.text2, "vence");
  icon(s, "clock", MX + 0.35, 1.8, 0.85, C.accent2, "vence");
  txt(s, "1 mes", { x: MX + 0.35, y: 2.9, w: 3.6, h: 1.0, fontSize: 60, bold: true, color: C.background1, objectName: "vence-n" });
  txt(s, "de vigencia para la web app en cuentas gratuitas. Se renueva con el botón «Run until 1 month from today» de la pestaña Web.", { x: MX + 0.35, y: 4.05, w: 3.6, h: 1.6, fontSize: 15, color: C.background1, objectName: "vence-texto" });
  [["Cómo afecta al CRUD", "Nuestra cuenta se creó cerca del 28-09-2026. Si nadie la renueva, PythonAnywhere deshabilita el sitio y el CRUD deja de estar disponible, aunque el código esté bien."],
   ["Cuenta posterior al 15-01-2026", "No incluye MySQL ni tareas programadas: la app debe usar SQLite, y PyMySQL queda instalado sin uso."],
   ["Otros límites del plan", "100 segundos de CPU al día, 512 MiB de disco e internet saliente solo hacia una lista de sitios permitidos."],
   ["Mitigación aplicada", "Vencía el 24-10-2026; la renovamos el 20-10 y ahora vence el 21-11-2026. Hay que renovarla cada mes y respaldar db.sqlite3."]].forEach(([h, b], i) => {
    const y = 1.45 + i * 1.27;
    card(s, 5.2, y, 7.53, 1.12, i === 3 ? "E6F2EC" : C.background2, "efecto-pa-" + i);
    txt(s, [{ text: h, options: { bold: true, fontSize: 15, color: i === 3 ? C.accent1 : C.text2, breakLine: true } }, { text: b, options: { fontSize: 13 } }], { x: 5.45, y: y + 0.12, w: 7.1, h: 0.92, objectName: "efecto-pa-texto-" + i });
  });
  source(s, "Es una restricción del plan, no una falla de seguridad. Fuentes: help.pythonanywhere.com/pages/FreeAccountsFeatures/ · blog.pythonanywhere.com/221/ (consultado 19-10-2026)");
  s.addNotes(`[ALEJANDRO · 30 s]
La limitación del plan gratuito: la web app vence al mes si nadie la renueva, y entonces el CRUD deja de estar disponible aunque el código esté bien. Nuestra app vencía el 24 de octubre; la renovamos y ahora vence el 21 de noviembre. Además, por la fecha de la cuenta, no tenemos MySQL y usamos SQLite. Es una restricción del plan, no una falla de seguridad.

Fuentes (no leer): https://help.pythonanywhere.com/pages/FreeAccountsFeatures/ · https://blog.pythonanywhere.com/221/`);

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
  s.addNotes(`[ALEJANDRO · 45 s]
En ética, dos acciones éticas: publicar los hallazgos reales, incluso los nuestros, sin excluir código para mejorar el resultado; y tratar el secreto como secreto: lo verificamos por hash y nunca lo mostramos.
Dos no éticas que evitamos: inventar resultados o excluir código para aprobar, y probar contra apps de otros usuarios o con datos reales. Por eso probamos en copia local con datos ficticios; en producción solo verificamos nuestra app con un usuario ficticio que borramos.
Como concientización proponemos un checklist de cinco minutos antes de cada push: sin secretos, check deploy, pruebas en verde y el .env fuera de git. Ya está en el README y lo presentaremos al curso.`);

  // ===================== 15. Conclusión =====================
  s = pres.addSlide({ masterName: "CIERRE", sectionTitle: "Ética y cierre" });
  txt(s, "CONCLUSIÓN DEL EQUIPO", { x: MX, y: 0.7, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 2, objectName: "kicker-conclusion" });
  s.addText("La herramienta orienta; la revisión y la evidencia deciden", { placeholder: "title" });
  [["gauge", "Aprobar no basta", "Los tres problemas más serios (clave débil, cantidad sin rango y typo CSRF) se confirmaron con revisión manual."],
   ["clip", "Un control se demuestra", "Requisito → prueba → control → evidencia, con commits trazables y ejecuciones guardadas."],
   ["lightbulb", "Aplicado en producción", "Clave rotada, dominio exacto, HTTPS forzado, Django 6.1.2 y app renovada. Pendiente: 6 code smells de mantenibilidad."]].forEach(([ic, h, b], i) => {
    const x = MX + i * 4.15, y = 2.55, w = 3.85, hh = 3.1;
    card(s, x, y, w, hh, "164A39", "cierre-" + i);
    icon(s, ic, x + 0.3, y + 0.3, 0.75, C.accent1, "cierre-icono-" + i);
    txt(s, h, { x: x + 0.3, y: y + 1.2, w: w - 0.6, h: 0.45, fontSize: 18, bold: true, color: C.background1, objectName: "cierre-titulo-" + i });
    txt(s, b, { x: x + 0.3, y: y + 1.7, w: w - 0.6, h: 1.3, fontSize: 14, color: C.accent5, objectName: "cierre-texto-" + i });
  });
  txt(s, "Gracias · ¿Preguntas?", { x: MX, y: 6.15, w: CW, h: 0.6, fontSize: 24, bold: true, color: C.accent2, objectName: "gracias" });
  s.addNotes(`[ALEJANDRO · 10 s] SonarQube nos orientó, pero los problemas más serios los confirmamos con revisión manual: aprobar el Quality Gate no basta.
[XAVIER · 15 s] Y un control vale si se puede demostrar: regla, prueba, control y evidencia. Las recomendaciones ya están aplicadas en producción y queda como mejora pendiente reducir seis alertas de mantenibilidad. Gracias, quedamos atentos a sus preguntas.`);

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
  s.addNotes("Anexo de referencia: no se expone. Todas las fuentes fueron consultadas el 19-10-2026.");

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("OK", OUT);
}
build().catch((e) => { console.error(e); process.exit(1); });
