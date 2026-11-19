// Recorrido del CRUD con un Chromium enrutado por el proxy de ZAP (equivale a la "Exploración manual"
// de ZAP Desktop, pero idéntico en el análisis inicial y en el final).
// Uso: LAB_USER=qa_ana LAB_PASSWORD=... node recorrido_navegador.mjs [proxy=127.0.0.1:8090 | directo] [base=http://127.0.0.1:8000]
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const PROXY = process.argv[2] || '127.0.0.1:8090';
const BASE = process.argv[3] || 'http://127.0.0.1:8000';
const USER = process.env.LAB_USER, PASS = process.env.LAB_PASSWORD;
if (!USER || !PASS) { console.error('Faltan LAB_USER y LAB_PASSWORD'); process.exit(2); }

const perfil = mkdtempSync(join(tmpdir(), 'zap-chromium-'));
const PORT = 9444;
const chrome = spawn('chromium', [...(process.env.VISIBLE ? [] : ['--headless=new']), `--remote-debugging-port=${PORT}`, `--user-data-dir=${perfil}`,
  ...(PROXY === 'directo' ? [] : [`--proxy-server=http://${PROXY}`, '--proxy-bypass-list=<-loopback>']),
  '--no-first-run', '--window-size=1400,900', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let ws;
for (let i = 0; i < 50 && !ws; i++) {
  try { ws = (await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json()).find((t) => t.type === 'page')?.webSocketDebuggerUrl; } catch {}
  await sleep(200);
}
const sock = new WebSocket(ws); await new Promise((r) => (sock.onopen = r));
let id = 0; const pend = new Map();
const violacionesCSP = [];
sock.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); }
  // Chromium informa las violaciones de la Content Security Policy como entradas del registro.
  if (m.method === 'Log.entryAdded' && /Content Security Policy/i.test(m.params.entry.text)) violacionesCSP.push(m.params.entry.text);
  if (m.method === 'Runtime.exceptionThrown') violacionesCSP.push('Excepción JS: ' + m.params.exceptionDetails.text);
};
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); sock.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (js) => (await send('Runtime.evaluate', { expression: js, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Page.enable'); await send('Log.enable'); await send('Runtime.enable');
// Los confirm() de los formularios se aceptan automáticamente.
await send('Page.addScriptToEvaluateOnNewDocument', { source: 'window.confirm = () => true;' });

const visitadas = [];
async function ir(ruta) { await send('Page.navigate', { url: BASE + ruta }); await sleep(1500); visitadas.push('GET ' + ruta); }
async function enviar(selector, campos, etiqueta) {
  const ok = await evaluate(`(() => { const f = document.querySelector(${JSON.stringify(selector)}); if (!f) return false;
    for (const [k, v] of Object.entries(${JSON.stringify(campos)})) { const el = f.querySelector('[name="' + k + '"]'); if (el) el.value = v; }
    HTMLFormElement.prototype.submit.call(f); return true; })()`);
  await sleep(1800); visitadas.push(`POST ${etiqueta}${ok ? '' : ' (formulario no encontrado)'}`);
}
const ruta = async () => evaluate('location.pathname');

await ir('/login/');
await enviar('form[method=post]:not([action*="/logout/"])', { username: USER, password: PASS }, 'login');
await ir('/');
await ir('/?sort=newest&q=Lista');
await ir('/lists/new/');
await enviar('form[method=post]:not([action*="/logout/"])', { name: 'Lista ZAP', priority: '1', budget_limit: '20000', description: 'Lista creada durante el análisis' }, 'crear lista');
const detalle = await ruta(); visitadas.push('(detalle) ' + detalle);
const pk = (detalle.match(/lists\/(\d+)/) || [])[1];
await enviar('form[action*="/items/add/"]', { name: 'Pan de prueba', quantity: '3', unit_price: '1200' }, 'agregar producto');
await enviar('form[action*="/items/add/"]', { name: 'Producto inválido', quantity: '0', unit_price: '1000' }, 'agregar producto con cantidad 0');
const itemPk = await evaluate(`(document.querySelector('form[action*="/toggle/"]')?.getAttribute('action').match(/items\\/(\\d+)/) || [])[1]`);
await enviar('form[action*="/toggle/"]', {}, 'marcar comprado');
await ir(`/lists/${pk}/?status=pending`);
await ir(`/items/${itemPk}/edit/`);
await enviar('form[method=post]:not([action*="/logout/"])', { name: 'Pan editado', quantity: '4', unit_price: '1300' }, 'editar producto');
await ir(`/lists/${pk}/edit/`);
await enviar('form[method=post]:not([action*="/logout/"])', { name: 'Lista ZAP editada', priority: '2' }, 'editar lista');
await enviar(`form[action*="/bulk-toggle/"]`, { action: 'check_all' }, 'marcar todos');
await ir(`/lists/${pk}/export-csv/`);
await ir(`/lists/${pk}/`);
await enviar('form[action*="/duplicate/"]', {}, 'duplicar lista');
await ir(`/lists/${pk}/`);
await enviar('form[action*="/clear-purchased/"]', {}, 'eliminar comprados');
await ir(`/lists/${pk}/delete/`);
await enviar('form[method=post]:not([action*="/logout/"])', {}, 'eliminar lista');
await ir('/');
await enviar('form[action*="/logout/"]', {}, 'logout');
await ir('/register/');
await ir(`/lists/${pk}/`); // ruta privada sin sesión: debe redirigir al login
console.log(visitadas.join('\n'));
console.log(`\nViolaciones de CSP o errores de JavaScript en el navegador: ${violacionesCSP.length}`);
violacionesCSP.forEach((v) => console.log('  ' + v));
sock.close(); chrome.kill(); await sleep(500); rmSync(perfil, { recursive: true, force: true });
