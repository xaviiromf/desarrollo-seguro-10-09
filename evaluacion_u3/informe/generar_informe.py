"""Genera informe.html (y luego PDF con Chromium) a partir de la evidencia en evaluacion_u3/evidencia/.

Uso: python generar_informe.py   ->  evaluacion_u3/informe/informe.html
"""
import html
import json
import pathlib

AQUI = pathlib.Path(__file__).parent
EVI = AQUI.parent / "evidencia"
U2 = AQUI.parent.parent / "evaluacion_u2" / "evidencia" / "sonarqube"
REPO = "https://github.com/xaviiromf/desarrollo-seguro-10-09"
PR = f"{REPO}/pull/1"
COMMIT_CODIGO = "132443b"
FECHA_CONSULTA = "18-11-2026"


def e(t):
    return html.escape(str(t))


def tabla(cabecera, filas, clase=""):
    th = "".join(f"<th>{c}</th>" for c in cabecera)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<table class="{clase}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def img(ruta, pie, ancho="100%"):
    return f'<figure><img src="{ruta}" style="width:{ancho}"><figcaption>{pie}</figcaption></figure>'


def codigo(texto, titulo=""):
    t = f'<div class="code-title">{titulo}</div>' if titulo else ""
    return f'{t}<pre class="code">{e(texto)}</pre>'


def leer(ruta):
    return (EVI / ruta).read_text()


def alertas(etapa):
    d = json.loads((EVI / "zap" / etapa / "reporte.json").read_text())
    return d["site"][0]["alerts"]


def sonar_despues():
    m = EVI / "sonarqube" / "despues_metricas.json"
    if not m.exists():
        return None
    met = {x["metric"]: x["value"] for x in json.loads(m.read_text())["component"]["measures"]}
    issues = json.loads((EVI / "sonarqube" / "despues_issues.json").read_text())["issues"]
    qg = json.loads((EVI / "sonarqube" / "despues_quality_gate.json").read_text())["projectStatus"]["status"]
    return met, issues, qg


# ---------------------------------------------------------------- secciones
def portada():
    return f"""
<section class="portada">
  <div class="kicker">Desarrollo Seguro · Evaluación Nº 3</div>
  <h1>CRUD Django con login, Docker y OWASP ZAP</h1>
  <p class="sub">Informe técnico · Aplicación «PastelMarket» (listas de compras)</p>
  {tabla(["", ""], [
      ["Integrantes", "Xavier Romero · Alejandro Figueroa"],
      ["Fecha de entrega", "19-11-2026"],
      ["Repositorio", f'<a href="{REPO}">{REPO}</a> (público)'],
      ["Pull Request", f'<a href="{PR}">{PR}</a>'],
      ["Versión revisada", f"Rama <code>evaluacion-u3</code>, código en el commit <code>{COMMIT_CODIGO}</code>; imagen <code>supermercado-lab:u3</code>"],
  ], "ficha")}
</section>"""


def s1():
    return f"""
<h2>1. Identificación y alcance</h2>
<p>Continuamos el CRUD de la Evaluación 2: una aplicación Django en la que cada usuario crea listas de compras y les agrega productos con cantidad y precio en pesos chilenos. En esta evaluación incorporamos y verificamos la autenticación, atendimos los hallazgos pendientes de SonarQube, ejecutamos la aplicación con Docker Compose y analizamos su tráfico con OWASP ZAP, corrigiendo lo confirmado.</p>
{tabla(["Elemento", "Detalle"], [
    ["Aplicación", "Django 6.1.2 · Python 3.12 · SQLite · gunicorn 26.2.0 · WhiteNoise 6.12.0"],
    ["Laboratorio", "Docker Compose en el equipo del equipo, publicado solo en <code>http://127.0.0.1:8000</code>"],
    ["Cuentas", "Ficticias: <code>qa_ana</code> y <code>qa_beto</code>, creadas con <code>manage.py crear_cuentas_prueba</code>; contraseñas solo en <code>.env.lab</code> (no versionado)"],
    ["Herramientas", "SonarQube Community Build 26.9.0.129388 (SAST) · OWASP ZAP 2.17.0 (DAST) · pruebas automatizadas de Django"],
    ["Fuera de alcance", "El despliegue público en PythonAnywhere <b>no</b> se escaneó, ni ningún sitio de terceros"],
])}
<p><b>Recorrido seguido:</b> (1) recuperar la evidencia de SonarQube de la Evaluación 2; (2) mejorar el código y verificar login y control de acceso; (3) construir y levantar el CRUD con Docker Compose; (4) análisis inicial de ZAP; (5) corregir y reconstruir el contenedor; (6) repetir las pruebas y el análisis para la comparación final.</p>"""


def s2():
    u2 = json.loads((U2 / "despues_issues.json").read_text())["issues"]
    decision = {
        ("python:S1192", 194): ("Media", "Corregir: constante <code>LIST_DETAIL_URL</code>"),
        ("python:S1192", 54): ("Media", "Corregir: constante <code>LIST_INDEX_URL</code>"),
        ("python:S1481", 374): ("Baja", "Corregir: eliminar la variable"),
        ("javascript:S3776", 59): ("Alta", "Corregir: dividir la función; al revisarla apareció un XSS en el DOM (2.3)"),
        ("javascript:S2486", 97): ("Media", "Corregir: registrar el error y volver al envío normal del formulario"),
        ("javascript:S6582", 23): ("Baja", "Corregir: encadenamiento opcional"),
    }
    filas = []
    for i in u2:
        clave = (i["rule"], i.get("line"))
        prio, dec = decision.get(clave, ("", ""))
        imp = ", ".join(f"{x['softwareQuality'].capitalize()}: {x['severity'].capitalize()}" for x in i.get("impacts", []))
        filas.append([f"<code>{i['rule']}</code>", f"<code>{i['component'].split(':', 1)[1]}:{i.get('line')}</code>",
                      e(i["message"]), f"{i['type'].replace('_', ' ').title()} · {imp}", prio, dec])
    sd = sonar_despues()
    if sd:
        met, issues, qg = sd
        abiertas = ", ".join(sorted({i["rule"] for i in issues})) or "ninguna"
        sonar_final = f"""<h3>2.2 Re-escaneo de verificación (18-11-2026)</h3>
        <p>El último análisis de la Evaluación 2 tenía 28 días y no incluía los cambios de esta evaluación, así que re-escaneamos el código final.
        El primer intento analizó también la carpeta de entrega <code>evaluacion_u3/</code> (informe, reportes HTML de ZAP y scripts), que no es código de la app:
        1.113 alertas ajenas y Quality Gate en ERROR. Agregamos <code>evaluacion_u3/**</code> a las exclusiones técnicas, igual que <code>evaluacion_u2/**</code> en la Evaluación 2.</p>
        <p>El análisis de la aplicación mostró <b>dos hallazgos nuevos</b>, introducidos por el código de esta evaluación, que corregimos:
        <code>docker:S6470</code> (vulnerabilidad, <i>Security High</i>): el <code>COPY . .</code> del Dockerfile podía meter archivos sensibles a la imagen; ahora se copian solo las carpetas de la app.
        Al revisarlo encontramos que <code>.dockerignore</code> excluía <code>node_modules/</code> solo en la raíz y se colaban 23 MB de dependencias de Node (<code>theme/static_src</code>); ahora no entran.
        <code>Web:InputWithoutLabelCheck</code> (bug): el <code>&lt;textarea hidden&gt;</code> del texto de WhatsApp no tenía etiqueta.</p>
        <p>Por último, la condición de cobertura del código nuevo fallaba (29,1 %). Agregamos pruebas al comando de cuentas de prueba y excluimos <b>solo de la cobertura</b>
        (los archivos siguen analizados) las migraciones, que son código generado, el script semilla <code>init_data.py</code> y el JavaScript, para el que el proyecto no tiene
        un framework de pruebas que genere el reporte; el JavaScript se verificó en el navegador (sección 6).</p>
        {tabla(["Métrica", "Evaluación 2 (20-10-2026)", "Evaluación 3 (18-11-2026)"], [
            ["Quality Gate", "Passed", f"<b>{qg.replace('OK', 'Passed')}</b> (cobertura de código nuevo 88,9 %)"],
            ["Vulnerabilidades · Bugs · Hotspots", "0 · 0 · 0", f"{met.get('vulnerabilities')} · {met.get('bugs')} · {met.get('security_hotspots')}"],
            ["Code smells", "6", f"<b>{met.get('code_smells')}</b> (abiertos: {e(abiertas)})"],
            ["Calificaciones (seguridad, confiabilidad, mantenibilidad)", "A · A · A", "A · A · A"],
            ["Cobertura total", "64,7 %", f"{met.get('coverage').replace('.', ',')} %"],
        ])}
        <div class="grid2">
        {img('../evidencia/sonarqube/captura_resumen_final.png', 'Re-escaneo final: Quality Gate aprobado, 0 issues abiertos y A en todo.')}
        {img('../evidencia/sonarqube/captura_issues_corregidos.png', 'Issues cerrados (Fixed) de las reglas tratadas. Los dos de generar_informe.py provienen del primer intento que incluyó la carpeta de entrega.')}
        </div>"""
    else:
        sonar_final = '<p class="pendiente"><b>Re-escaneo de SonarQube pendiente</b> de iniciar sesión en el panel local; las correcciones están en el código y en el commit indicado.</p>'
    return f"""
<h2>2. SonarQube y login</h2>
<h3>2.1 Hallazgos heredados de la Evaluación 2</h3>
<p>Partimos del último análisis de la Evaluación 2 (SonarQube 26.9, 20-10-2026): Quality Gate aprobado, 0 vulnerabilidades, 0 security hotspots y <b>6 code smells pendientes</b>. Al no haber hotspots no hubo revisión contextual que hacer; recordamos que un hotspot exige revisión y no confirma por sí solo una vulnerabilidad. No agregamos exclusiones: solo se excluyen carpetas técnicas (entorno virtual, dependencias, archivos generados y la carpeta de entrega).</p>
{tabla(["Regla", "Archivo", "Problema", "Tipo e impacto", "Prioridad", "Decisión técnica"], filas, "small")}
{sonar_final}
<h3>2.3 Defectos reales encontrados al corregir</h3>
<p>Al refactorizar la función que SonarQube marcaba por complejidad (<code>javascript:S3776</code>) encontramos un <b>XSS en el DOM</b> que la herramienta no señaló: al marcar un producto como comprado, el script tomaba el nombre con <code>textContent</code> (texto sin escapar) y lo volvía a insertar con <code>innerHTML</code>. Un producto llamado <code>&lt;img src=x onerror=…&gt;</code> ejecutaría código.</p>
{codigo("""if (data.is_purchased) {
    nameCell.innerHTML = `<s>${nameCell.textContent.trim()}</s>`;   // texto del usuario como HTML
}""", "Antes · static/shopping/js/calculator.js")}
{codigo("""function applyPurchasedState(row, isPurchased) {
    const name = nameCell.textContent.trim();
    if (isPurchased) {
        const strike = document.createElement('s');
        strike.textContent = name;            // siempre como texto, nunca como HTML
        nameCell.replaceChildren(strike);
    } else {
        nameCell.replaceChildren(document.createTextNode(name));
    }
}""", "Después · commit 5ccd32a")}
<p>También corregimos un defecto funcional en las vistas de eliminación: desde Django 4, <code>DeleteView</code> procesa el POST en <code>form_valid()</code> y ya no llama a <code>delete()</code>, por lo que los mensajes de confirmación nunca se mostraban. La prueba <code>test_eliminar_producto_propio_muestra_mensaje</code> falla con el código anterior y pasa con el corregido.</p>

<h3>2.4 Autenticación y acceso al CRUD</h3>
<p>El proyecto ya tenía login y control de acceso con el sistema de autenticación de Django. Los revisamos contra cada requisito y escribimos <b>12 pruebas nuevas</b> que los demuestran.</p>
{tabla(["Requisito", "Cómo se cumple", "Prueba"], [
    ["Login con credenciales válidas", "<code>LoginView</code> de Django (<code>UserLoginView</code>)", "<code>test_login_valido_redirige_y_crea_sesion</code>"],
    ["Rechazar credenciales inválidas", "Formulario de autenticación de Django; no crea sesión", "<code>test_login_invalido_rechazado_sin_sesion</code>"],
    ["Cerrar sesión por POST con CSRF", "<code>LogoutView</code> solo acepta POST; el formulario lleva <code>{% csrf_token %}</code>", "GET → 405 · POST sin token → 403 · POST con token → cierra sesión"],
    ["Rutas privadas protegidas en el servidor", "<code>LoginRequiredMixin</code> en las 14 vistas del CRUD", "<code>test_anonimo_redirigido_al_login_en_rutas_privadas</code>, <code>test_anonimo_no_puede_escribir</code>"],
    ["Permiso por registro al consultar y escribir", "<code>get_queryset()</code> y <code>get_object_or_404(..., user=request.user)</code>: lo ajeno responde 404", "<code>test_intruso_no_puede_consultar_ni_modificar_lista_ajena</code> (9 casos), <code>…producto_ajeno</code> (4 casos)"],
    ["Panel de administración", "Exige <code>is_staff</code>", "<code>test_admin_exige_staff</code>"],
], "small")}
<p><b>Matriz de acceso.</b> El <b>dueño</b> consulta, crea, edita, duplica, exporta y elimina solo sus listas y productos. <b>Otro usuario autenticado</b> no ve ni modifica datos ajenos (404, sin revelar si el registro existe). Un <b>anónimo</b> solo accede al login y al registro. El <b>administrador</b> (<code>is_staff</code>) usa el panel <code>/admin/</code>. Ocultar botones no es el control: la autorización ocurre en el servidor y las pruebas envían las peticiones directamente.</p>
<p><b>Registro abierto (decisión):</b> lo mantenemos, porque la aplicación es de uso personal y una cuenta nueva no obtiene acceso a datos ajenos. Riesgo residual: creación masiva de cuentas; mejora futura: CAPTCHA o verificación por correo.</p>
{tabla(["Resultado de las 12 pruebas", "Código de la Evaluación 2", "Código corregido"], [
    ["Login, logout, CSRF, anónimo y permisos (11 pruebas)", "11 pasan: los controles ya eran correctos", "11 pasan"],
    ["Mensaje al eliminar un producto (1 prueba)", "<span class=bad>Falla</span>: el mensaje nunca se mostraba", "<span class=good>Pasa</span>"],
])}
<div class="grid2">
{img('../evidencia/capturas/02_login_incorrecto.png', 'Login con contraseña incorrecta: rechazado, sin sesión.')}
{img('../evidencia/capturas/03_login_correcto_lista.png', 'Login correcto: el usuario ve solo sus listas.')}
</div>
<div class="grid2">
{img('../evidencia/capturas/01_ruta_protegida_redirige_login.png', 'Petición directa a <code>/lists/1/</code> sin sesión: redirige al login.')}
{img('../evidencia/capturas/05_lista_inexistente_o_ajena_404.png', 'Lista inexistente o ajena: 404, sin revelar si existe.')}
</div>
{codigo('$ curl -s -o /dev/null -w "%{http_code} %{redirect_url}" http://127.0.0.1:8000/          # ruta privada, sin sesión' + chr(10) + '302 http://127.0.0.1:8000/login/?next=/' + chr(10) + chr(10) + '$ curl -s -o /dev/null -w "%{http_code} %{redirect_url}" http://127.0.0.1:8000/lists/1/delete/ -X POST' + chr(10) + '403   # sin sesión ni token CSRF: rechazado antes de llegar a la vista', 'Peticiones directas con curl a rutas protegidas (laboratorio Docker)')}"""


def s3():
    return f"""
<h2>3. Datos sensibles, sesiones e industrias</h2>
<h3>3.1 Inventario de activos</h3>
{tabla(["Activo", "Dónde está", "Quién debería acceder", "Riesgo", "Solución tentativa", "Control"], [
    ["<b>Correo y nombre de usuario</b> (dato personal)", "Tabla <code>auth_user</code>", "El propio usuario y el administrador", "Que otro usuario o un tercero lo consulte o lo extraiga", "Minimización: el correo es opcional; no se muestra a otros usuarios", "<span class=good>Aplicado</span>"],
    ["<b>Contraseña</b>", "<code>auth_user.password</code>", "Nadie en texto: solo se verifica", "Robo de la base y uso de las contraseñas en otros sitios", "Hash PBKDF2-SHA256 con 1.500.000 iteraciones y sal; validadores de contraseña", "<span class=good>Aplicado</span>"],
    ["<b>Listas, productos y presupuestos</b> (registro del negocio)", "Tablas <code>shopping_*</code>", "Solo el dueño", "Que otro usuario lea o modifique hábitos de compra y presupuestos", "Autorización por registro en el servidor (404 a lo ajeno)", "<span class=good>Aplicado y probado</span>"],
    ["<b>Sesión</b>", "Cookie <code>sessionid</code> + tabla <code>django_session</code>", "Solo el navegador del usuario", "Robo de la cookie y suplantación", "HttpOnly, SameSite=Lax, expiración de 14 días; Secure en producción", "<span class=good>Aplicado</span>; Secure solo con HTTPS"],
    ["<b>Exportación CSV</b>", "Respuesta de <code>/lists/&lt;id&gt;/export-csv/</code>", "Solo el dueño de la lista", "Extracción masiva de datos de otra cuenta", "Misma autorización por registro; no se guarda en caché", "<span class=good>Aplicado</span>"],
    ["<b>Clave secreta y contraseñas de prueba</b>", "Variables de entorno (<code>.env</code>, <code>.env.lab</code>)", "Solo el servidor", "Firmar sesiones falsas si se filtra", "Fuera de git y de la imagen Docker (<code>.dockerignore</code>)", "<span class=good>Aplicado</span>"],
], "small")}
<h3>3.2 Mecanismos de protección: propósito y límites</h3>
{tabla(["Mecanismo", "Propósito en este CRUD", "Límite"], [
    ["Minimización", "Pedir solo lo necesario: el correo es opcional", "No protege lo que sí se guarda"],
    ["Autorización", "Cada consulta se filtra por el usuario de la sesión", "Depende de que todas las vistas la apliquen; por eso hay pruebas por cada ruta"],
    ["Hash de contraseñas", "Ni nosotros podemos leer la contraseña", "Una contraseña débil igual puede adivinarse; no reemplaza limitar los intentos"],
    ["Enmascaramiento", "Útil para mostrar el correo parcialmente en una vista", "Ocultarlo en una plantilla no impide que una exportación o una API revele el valor original"],
    ["Cifrado en reposo", "No lo aplicamos: los datos no tienen una sensibilidad que lo justifique", "Si la base se usara para salud o pagos sí haría falta (3.3)"],
], "small")}
<h3>3.3 Comparación de dos industrias: el historial de compras</h3>
{tabla(["Aspecto", "Comercio minorista (supermercado)", "Salud (farmacia)"], [
    ["Dato y uso", "Productos, cantidades y montos de cada lista, para planificar compras", "Los mismos campos, pero los productos son medicamentos o insumos médicos"],
    ["Daño por exposición", "Revela hábitos de consumo; daño moderado (publicidad no deseada, perfilamiento)", "Revela condiciones de salud (dato sensible): discriminación laboral o de seguros, daño grave y difícil de revertir"],
    ["Acceso y exportación", "El dueño puede exportar libremente su CSV", "Exportación restringida, justificada y registrada; acceso del personal solo por necesidad clínica"],
    ["Auditoría", "No se exige registrar cada consulta", "Registro de quién accedió a cada historial y cuándo"],
    ["Control y límite", "Autorización por registro (ya implementada). No cubre al administrador, que ve todo", "Autorización más cifrado en reposo, auditoría y minimización estricta. Ni el cifrado ni la auditoría impiden el abuso de un usuario autorizado: solo lo dejan registrado"],
], "small")}
<h3>3.4 Sesiones y cookies</h3>
<p>El proyecto usa el backend <code>django.contrib.sessions.backends.db</code>: la información de la sesión (id del usuario y hash de verificación) se guarda en la tabla <code>django_session</code>, y el navegador solo recibe la clave aleatoria en la cookie <code>sessionid</code>. Al cerrar sesión el registro se invalida en el servidor.</p>
{tabla(["Cookie", "Para qué sirve", "Atributos en el laboratorio (HTTP)", "En producción (HTTPS)"], [
    ["<code>sessionid</code>", "Identifica la sesión", "HttpOnly · SameSite=Lax · 14 días", "Además <b>Secure</b> y HSTS"],
    ["<code>csrftoken</code>", "Protección CSRF", "<b>HttpOnly</b> (corregido, 6.1) · SameSite=Lax", "Además Secure"],
    ["<code>messages</code>", "Mensajes de una sola lectura", "HttpOnly · SameSite=Lax · firmada", "Además Secure"],
], "small")}
{codigo(leer('sesiones/01_sesiones_y_cookies.txt').split('## Set-Cookie')[1].split('##')[0].strip(), 'Cabeceras Set-Cookie al iniciar sesión (valores ocultos)')}
<p>Las cookies <code>Secure</code> están desactivadas <b>solo</b> en el perfil de laboratorio, porque usa HTTP en 127.0.0.1; en producción van activadas por variable de entorno. Lo registramos como comportamiento contextual.</p>"""


def diagrama():
    return """
<svg viewBox="0 0 900 250" class="diagrama" role="img" aria-label="Diagrama del laboratorio">
  <defs><marker id="f" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#35607D"/></marker></defs>
  <rect x="10" y="20" width="560" height="210" rx="10" fill="#EEF5F1" stroke="#9CCBB4"/>
  <text x="25" y="42" class="z">Equipo anfitrión (Linux)</text>
  <rect x="30" y="80" width="140" height="70" rx="8" fill="#fff" stroke="#1F7A5A"/><text x="100" y="110" class="t">Navegador</text><text x="100" y="128" class="s">Chromium</text>
  <rect x="215" y="80" width="150" height="70" rx="8" fill="#fff" stroke="#1F7A5A"/><text x="290" y="110" class="t">OWASP ZAP 2.17.0</text><text x="290" y="128" class="s">proxy 127.0.0.1:8090</text>
  <rect x="410" y="80" width="140" height="70" rx="8" fill="#fff" stroke="#B8452F"/><text x="480" y="110" class="t">Puerto publicado</text><text x="480" y="128" class="s">127.0.0.1:8000</text>
  <rect x="610" y="20" width="280" height="210" rx="10" fill="#E6F0F6" stroke="#35607D"/>
  <text x="625" y="42" class="z">Docker Compose · red interna</text>
  <rect x="635" y="70" width="230" height="70" rx="8" fill="#fff" stroke="#35607D"/><text x="750" y="98" class="t">Contenedor web</text><text x="750" y="116" class="s">gunicorn :8000 · usuario app · solo lectura</text>
  <rect x="635" y="160" width="230" height="55" rx="8" fill="#fff" stroke="#35607D"/><text x="750" y="185" class="t">Volumen lab_data</text><text x="750" y="202" class="s">/data/db.sqlite3</text>
  <line x1="170" y1="115" x2="213" y2="115" stroke="#35607D" stroke-width="2" marker-end="url(#f)"/>
  <line x1="365" y1="115" x2="408" y2="115" stroke="#35607D" stroke-width="2" marker-end="url(#f)"/>
  <line x1="550" y1="115" x2="633" y2="105" stroke="#35607D" stroke-width="2" marker-end="url(#f)"/>
  <line x1="750" y1="140" x2="750" y2="158" stroke="#35607D" stroke-width="2" marker-end="url(#f)"/>
  <text x="290" y="175" class="s">URL objetivo: http://127.0.0.1:8000</text>
</svg>"""


def s4():
    df = (AQUI.parent.parent / "Dockerfile").read_text()
    cy = (AQUI.parent.parent / "compose.yaml").read_text()
    return f"""
<h2>4. Ejecución del CRUD desde Docker</h2>
<h3>4.1 Diagrama y acceso de ZAP</h3>
{diagrama()}
<p>El navegador y ZAP se ejecutan en el equipo anfitrión. El navegador usa ZAP como proxy y llega al CRUD por <code>http://127.0.0.1:8000</code>, el único puerto publicado, ligado solo a la interfaz local. Ese puerto conduce al contenedor <code>web</code> (gunicorn), que guarda la base SQLite del laboratorio en el volumen <code>lab_data</code>. ZAP analiza esta instancia, no un <code>runserver</code> del anfitrión ni el despliegue público.</p>
<h3>4.2 Archivos del laboratorio</h3>
{tabla(["Archivo", "Qué hace y por qué es seguro"], [
    ["<code>Dockerfile</code>", "Imagen oficial <code>python:3.12-slim</code> (misma serie que producción), dependencias con versiones fijas desde <code>requirements.txt</code>, estáticos recopilados al construir, <b>usuario sin privilegios</b> (uid 10001) y healthcheck"],
    ["<code>compose.yaml</code>", "Servicio <code>web</code> con el puerto <b>solo en 127.0.0.1:8000</b>, sistema de archivos de solo lectura, <code>no-new-privileges</code>, sin capacidades de Linux, volumen para SQLite y reinicio automático"],
    ["<code>.env.lab.example</code>", "Perfil de laboratorio diferenciado: <code>DEBUG=False</code>, <code>ALLOWED_HOSTS=127.0.0.1,localhost</code>, secretos y contraseñas de prueba por variables (valores de ejemplo, sin secretos)"],
    ["<code>.dockerignore</code> / <code>.gitignore</code>", "Excluyen <code>.env*</code>, bases de datos, entornos virtuales, cachés y archivos ajenos a la construcción"],
    ["<code>docker/entrypoint.sh</code>", "Aplica migraciones y arranca gunicorn (laboratorio de una instancia)"],
    ["<code>README.md</code>", "Requisitos, construcción, arranque, migraciones, cuentas de prueba, URL y pruebas"],
], "small")}
<p>Respecto del material de apoyo del docente mantuvimos el patrón (imagen slim, volumen para SQLite, WhiteNoise, puerto en 127.0.0.1) y mejoramos: usuario no root, gunicorn en lugar del servidor de desarrollo, versiones fijas y endurecimiento del contenedor.</p>
<div class="grid2">{codigo(df.split('# Estáticos')[0].strip() + chr(10) + '...', 'Dockerfile (extracto)')}{codigo(cy.strip(), 'compose.yaml')}</div>
<h3>4.3 Versiones y comprobación del entorno</h3>
{codigo(leer('docker/03_versiones_y_endurecimiento.txt').split('# Versiones del laboratorio')[1].strip(), 'Versiones, usuario del proceso, solo lectura y check --deploy dentro del contenedor')}
<p>Los cuatro avisos de <code>check --deploy</code> corresponden a HTTPS (HSTS, redirección y cookies Secure) y son esperables en un laboratorio HTTP; no aparecen los de clave débil ni de <code>DEBUG</code>.</p>
{codigo(leer('docker/02_servicio_en_ejecucion.txt').split('(fecha')[1].split('\n', 1)[1].split('$ curl -s -o')[0].strip(), 'docker compose ps y cabeceras desde el puerto publicado')}
{img('../evidencia/capturas/04_detalle_lista.png', 'El CRUD operativo desde el contenedor, en http://127.0.0.1:8000.', '82%')}"""


ORIGEN = {
    "10038": ("Aplicación propia", "Confirmado", "Media", "Sin CSP, una inyección de script no tiene una segunda barrera"),
    "10098": ("Tercero (WhiteNoise, configuración por defecto)", "Confirmado (bajo impacto: son archivos públicos)", "Baja", "Cualquier origen puede leer los estáticos por CORS"),
    "10010": ("Aplicación propia (configuración de Django)", "Confirmado", "Baja", "Un script inyectado podría leer el token CSRF"),
    "10111": ("Aplicación propia", "Contextual (informativo)", "—", "ZAP reconoce el formulario de login"),
    "10112": ("Aplicación propia", "Contextual (informativo)", "—", "ZAP reconoce la cookie de sesión"),
    "10031": ("Aplicación propia", "Falso positivo justificado (verificado a mano, 5.3)", "—", "El valor vuelve escapado"),
}


def tabla_zap(etapa):
    filas = []
    for n, a in enumerate(alertas(etapa), 1):
        inst = a["instances"][0]
        cwe = f"CWE-{a['cweid']}" if str(a.get("cweid")) not in ("-1", "0", "") else "—"
        org, dec, prio, imp = ORIGEN.get(a["pluginid"], ("", "", "", ""))
        param = inst.get("param") or "—"
        evid = inst.get("evidence") or ("(cabecera ausente)" if a["pluginid"] == "10038" else "(valor reflejado; ver 5.3)")
        filas.append([f"Z{n}", f"{a['pluginid']} · {e(a['name'])}", e(a["riskdesc"]),
                      f"{inst['method']} <code>{e(inst['uri'].replace('http://127.0.0.1:8000', ''))}</code> · {e(param)} ({a['count']} inst.)",
                      f"<code>{e(evid[:60])}</code>", org, dec, prio, cwe])
    return tabla(["ID", "Regla ZAP", "Riesgo (confianza)", "Ruta · parámetro", "Evidencia", "Origen", "Decisión", "Prioridad", "CWE"], filas, "xs")


def s5():
    urls = leer("zap/inicial/urls_visitadas.txt").splitlines()
    rutas = sorted({u.replace("http://127.0.0.1:8000", "").split("?")[0] for u in urls[1:]})
    return f"""
<h2>5. Análisis inicial con OWASP ZAP</h2>
<h3>5.1 Alcance y cobertura</h3>
{tabla(["Elemento", "Valor"], [
    ["Sesión ZAP", "<code>u3_inicial</code> (nueva, solo para esta revisión) · 18-11-2026 14:48"],
    ["Contexto", "<code>CRUD-laboratorio</code>, incluye solo <code>http://127\\.0\\.0\\.1:8000.*</code>"],
    ["Objetivo", "<code>http://127.0.0.1:8000</code>, imagen <code>supermercado-lab:u3</code> con login y correcciones de SonarQube, antes de las correcciones motivadas por ZAP"],
    ["Recorrido", "Navegador Chromium enrutado por el proxy de ZAP con la cuenta ficticia <code>qa_ana</code>: login, listas (crear, buscar, editar, duplicar, exportar CSV, eliminar), productos (agregar, uno con cantidad 0, editar, marcar, eliminar comprados), logout, registro y una ruta privada sin sesión. Se automatizó con <code>evaluacion_u3/herramientas/recorrido_navegador.mjs</code> para repetir exactamente las mismas acciones en el análisis final"],
    ["Análisis", "Pasivo, esperando a que la cola de ZAP llegara a 0. ZAP 2.17.0 en modo daemon para el análisis inicial y final; verificación adicional en ZAP Desktop (6.2)"],
    ["Cobertura", f"{len(urls) - 1} URLs del objetivo registradas ({len(rutas)} rutas distintas). El árbol Sites contiene <b>solo</b> 127.0.0.1:8000: el perfil limpio del navegador no generó tráfico a terceros"],
    ["Reportes", "<code>evidencia/zap/inicial/</code>: <code>reporte.html</code> (legible), <code>reporte.json</code> y <code>reporte.md</code> (estructurados), filtrados al objetivo"],
], "small")}
<p class="small">Rutas visitadas: {", ".join(f"<code>{e(r)}</code>" for r in rutas)}</p>
{img('../evidencia/capturas/zap_inicial_resumen.png', 'Resumen del reporte inicial de ZAP: 2 alertas de riesgo medio, 1 baja y 3 informativas.', '78%')}
<h3>5.2 Tabla de hallazgos de ZAP</h3>
{tabla_zap('inicial')}
<p class="small">Evidencia de petición y respuesta (sin secretos): en la respuesta de <code>GET /login/</code> no hay cabecera <code>Content-Security-Policy</code>; <code>GET /static/css/dist/styles.css</code> responde <code>Access-Control-Allow-Origin: *</code>; <code>Set-Cookie: csrftoken=…; SameSite=Lax</code> sin <code>HttpOnly</code>. El detalle completo de cada instancia está en <code>reporte.html</code>.</p>
<h3>5.3 Hallazgos de la revisión manual (no detectados por ZAP)</h3>
<p>El análisis pasivo no prueba entradas maliciosas, así que revisamos a mano cómo se usan los datos del usuario en las plantillas.</p>
{tabla(["ID", "Hallazgo", "Ubicación", "Verificación", "Origen", "Decisión", "Prioridad", "Referencia"], [
    ["M1", "XSS almacenado: el nombre del producto dentro de <code>onsubmit=\"return confirm('…')\"</code>. El navegador decodifica el escape HTML (<code>&amp;#x27;</code> → <code>'</code>) antes de ejecutar el JavaScript", "<code>shoppinglist_detail.html:310</code>", "Confirmado en el laboratorio: un producto <code>x'+(document.title='XSS-ejecutado')+'</code> ejecutó código al intentar borrarlo", "Aplicación propia", "Confirmado", "Alta", "CWE-79"],
    ["M2", "Datos del usuario dentro de cadenas de un <code>&lt;script&gt;</code> en línea con escape HTML (contexto incorrecto)", "<code>shoppinglist_detail.html</code> (texto de WhatsApp)", "Revisión de código: un nombre con <code>\\</code> rompe la cadena", "Aplicación propia", "Requiere investigación → se corrige preventivamente", "Media", "CWE-79"],
    ["M3", "Credenciales <code>admin</code>/<code>admin</code> publicadas en la página de login y escritas en <code>init_data.py</code>", "<code>registration/login.html</code>, <code>init_data.py</code>", "Visible en la página pública", "Aplicación propia", "Confirmado", "Alta", "CWE-798"],
    ["M4", "Páginas privadas sin <code>Cache-Control</code>: el navegador podía guardar datos del usuario", "Todas las vistas con sesión", "<code>curl -I</code> con sesión: sin <code>Cache-Control</code>", "Aplicación propia", "Confirmado (preventivo)", "Media", "CWE-524"],
    ["M5", "Alerta 10031: <code>q</code> y <code>sort</code> se reflejan en atributos", "<code>/?q=…&amp;sort=…</code>", "Con <code>q=\"&gt;&lt;script&gt;…</code> la respuesta sale escapada (<code>&amp;quot;&amp;gt;&amp;lt;script…</code>)", "Aplicación propia", "Falso positivo justificado", "—", "CWE-20"],
], "xs")}
{codigo(leer('manual/01_antes_xss_onsubmit.txt').split('\n\n', 1)[1].strip(), 'M1 · Prueba controlada antes de la corrección (laboratorio, cuenta ficticia)')}
<h3>5.4 Amenazas del proyecto (STRIDE)</h3>
{tabla(["Categoría", "Activo", "Actor", "Acción", "Impacto", "Prioridad", "Control"], [
    ["<b>S</b> · Suplantación", "Cuenta y sesión", "Atacante externo", "Probar contraseñas en <code>/login/</code> o usar las credenciales publicadas (M3)", "Acceso a las listas de la víctima o al panel de administración", "Alta", "Credenciales retiradas (M3), validadores de contraseña, hash PBKDF2. <b>Pendiente:</b> limitar intentos de login"],
    ["<b>T</b> · Manipulación", "Listas y productos", "Usuario autenticado malicioso", "Enviar POST directos para modificar datos de otro usuario", "Alteración de datos ajenos", "Alta", "Autorización por registro en el servidor; 13 casos de prueba devuelven 404"],
    ["<b>I</b> · Divulgación de información", "Historial de compras, CSV", "Otro usuario o equipo compartido", "Abrir <code>/lists/&lt;id&gt;/export-csv/</code> ajeno o ver páginas en caché tras el logout", "Exposición de hábitos y presupuestos", "Media", "404 a lo ajeno; <code>Cache-Control: private, no-store</code> (M4)"],
    ["<b>E</b> · Elevación de privilegios", "Sesión del usuario", "Atacante que logra que la víctima vea un producto manipulado", "XSS almacenado (M1) para actuar con la sesión de la víctima", "Acciones en nombre de la víctima", "Alta", "Escape correcto por contexto, sin manejadores en línea, CSP sin <code>unsafe-inline</code>"],
    ["<b>R</b> · Repudio", "Acciones sobre listas", "Usuario legítimo", "Negar haber borrado una lista", "Sin trazabilidad", "Baja", "<b>Pendiente:</b> registro de auditoría (no exigido para este dato; sí en salud, 3.3)"],
], "xs")}
<p>Las fallas de autorización (T e I) no las señala ZAP en un análisis pasivo; por eso las verificamos con pruebas manuales y automatizadas.</p>"""


def s6():
    ini = {a["pluginid"]: a for a in alertas("inicial")}
    fin = {a["pluginid"]: a for a in alertas("final")}
    estado = {"10038": "<span class=good>Resuelto</span>", "10098": "<span class=good>Resuelto</span>", "10010": "<span class=good>Resuelto</span>",
              "10111": "Contextual", "10112": "Contextual", "10031": "Falso positivo"}
    comp = [[f"{pid} · {e(a['name'])}", e(a["riskdesc"]), str(a["count"]),
             str(fin[pid]["count"]) if pid in fin else "0", estado.get(pid, "")] for pid, a in ini.items()]
    return f"""
<h2>6. Correcciones y verificación final</h2>
<h3>6.1 Remediación priorizada</h3>
{tabla(["Hallazgo", "Causa", "Cambio", "Commit", "Prueba", "Resultado"], [
    ["M1 XSS en <code>onsubmit</code> (Alta)", "Dato del usuario en JavaScript dentro de un atributo", "Texto en <code>data-confirm</code>, leído como dato por <code>static/shopping/js/ui.js</code>", "<code>b73372e</code>", "Misma carga en el laboratorio + <code>test_nombre_de_producto_no_llega_a_codigo_ejecutable</code>", "<span class=good>Resuelto</span>: se muestra como texto"],
    ["M3 Credenciales publicadas (Alta)", "Aviso de ayuda en la plantilla y contraseñas en el script semilla", "Aviso eliminado; <code>init_data.py</code> lee las contraseñas del entorno", "<code>c35d594</code>", "<code>test_login_no_publica_credenciales</code>", "<span class=good>Resuelto</span>"],
    ["Z1 / 10038 CSP ausente (Media)", "No había política", "CSP nativa de Django 6: <code>default-src 'self'</code>, sin <code>unsafe-inline</code>, <code>frame-ancestors 'none'</code>. Código y estilos en línea movidos a <code>ui.js</code> y <code>print.css</code>", "<code>b73372e</code>", "Recorrido completo en Chromium: <b>0 violaciones de CSP y 0 errores de JavaScript</b>; <code>test_csp_presente_y_sin_codigo_en_linea</code>", "<span class=good>Resuelto</span>"],
    ["M2 Script en línea (Media)", "Escape HTML dentro de cadenas JavaScript", "El texto de WhatsApp lo arma el servidor en un <code>&lt;textarea hidden&gt;</code> (escape HTML correcto ahí)", "<code>b73372e</code>", "Sin <code>&lt;script&gt;</code> en la página (prueba)", "<span class=good>Resuelto</span>"],
    ["M4 Caché de páginas privadas (Media)", "Sin cabecera", "<code>PrivateNoStoreMiddleware</code>: <code>Cache-Control: private, no-store</code> con sesión", "<code>b73372e</code>", "<code>test_paginas_privadas_no_se_guardan_en_cache</code>", "<span class=good>Resuelto</span>"],
    ["Z2 / 10098 CORS en estáticos (Baja)", "Valor por defecto de WhiteNoise", "<code>WHITENOISE_ALLOW_ALL_ORIGINS = False</code>", "<code>b73372e</code>", "<code>curl -I</code> al estático: sin <code>Access-Control-Allow-Origin</code>", "<span class=good>Resuelto</span>"],
    ["Z3 / 10010 csrftoken sin HttpOnly (Baja)", "Valor por defecto de Django", "<code>CSRF_COOKIE_HTTPONLY = True</code> (el JavaScript toma el token del formulario)", "<code>b73372e</code>", "<code>test_cookie_csrf_httponly</code>", "<span class=good>Resuelto</span>"],
], "xs")}
<div class="grid2">
{codigo('''<form action="{% url 'shopping:item_delete' item.id %}" method="post"
      onsubmit="return confirm('¿Eliminar {{ item.name }}?');">''', 'Antes · shoppinglist_detail.html')}
{codigo('''<form action="{% url 'shopping:item_delete' item.id %}" method="post"
      data-confirm="¿Eliminar {{ item.name }}?">

// static/shopping/js/ui.js
form.addEventListener('submit', (e) => {
    if (!window.confirm(form.dataset.confirm)) e.preventDefault();
});''', 'Después · plantilla + ui.js')}
</div>
{codigo('''SECURE_CSP = {
    "default-src": [CSP.SELF], "script-src": [CSP.SELF], "style-src": [CSP.SELF],
    "img-src": [CSP.SELF, "data:"], "form-action": [CSP.SELF],
    "frame-ancestors": [CSP.NONE], "base-uri": [CSP.SELF], "object-src": [CSP.NONE], ...
}
CSRF_COOKIE_HTTPONLY = True
WHITENOISE_ALLOW_ALL_ORIGINS = False''', 'supermarket_project/settings.py (después)')}
{codigo(leer('manual/02_despues_xss_onsubmit.txt').split('\n\n', 1)[1].strip(), 'M1 · Misma prueba después de la corrección')}
<h3>6.2 Segundo análisis y comparación</h3>
<p>Repetimos el análisis en una <b>sesión nueva</b> (<code>u3_final</code>, 18-11-2026) con el mismo contexto, la misma cuenta y el mismo recorrido automatizado. Comparamos las acciones de ambos recorridos y son idénticas, así que ninguna alerta desapareció por dejar de visitar una ruta.</p>
{tabla(["Alerta ZAP", "Riesgo", "Instancias inicial", "Instancias final", "Estado"], comp)}
<div class="grid2">
{img('../evidencia/capturas/zap_inicial_resumen.png', 'Reporte inicial.')}
{img('../evidencia/capturas/zap_final_resumen.png', 'Reporte final: solo alertas informativas.')}
</div>
<p><b>Verificación complementaria en ZAP Desktop.</b> Repetimos el recorrido con ZAP Desktop 2.17.0 (interfaz gráfica), sesión <code>u3_desktop</code> y contexto <code>CRUD-laboratorio</code>, con un Chromium visible enrutado por su proxy: 69 mensajes, el árbol Sites contiene solo el objetivo y no hay alertas altas, medias ni bajas (solo las 3 informativas). Reporte en <code>evidencia/zap/desktop/</code>.</p>
{img('../evidencia/zap/desktop/zap_desktop_sesion.png', 'ZAP Desktop: contexto CRUD-laboratorio, Sites solo con 127.0.0.1:8000, historial del recorrido por el proxy y barra de alertas (0 · 0 · 0 · 3).', '92%')}
<p><b>Pruebas automatizadas:</b> 44 pruebas pasan (validación de la Evaluación 2, autenticación y autorización, cabeceras, XSS y el comando de cuentas de prueba).</p>
<h3>6.3 Pendientes y riesgos que permanecen</h3>
<ul>
<li><b>Limitar los intentos de login</b> (fuerza bruta): pendiente; candidato <code>django-axes</code> o limitación en el proxy.</li>
<li><b>Cookies Secure y HSTS en el laboratorio:</b> contextual, porque usa HTTP; en producción están activos.</li>
<li><b>Registro abierto:</b> riesgo aceptado (creación masiva de cuentas).</li>
<li><b>Auditoría de acciones</b> (repudio): no implementada.</li>
<li><b>Cobertura del JavaScript:</b> sin pruebas automatizadas propias (excluido solo de la métrica de cobertura); se verifica en navegador.</li>
</ul>"""


def s7():
    return f"""
<h2>7. Conclusiones técnicas</h2>
<p><b>SAST frente a DAST.</b> SonarQube (SAST) lee el código sin ejecutarlo: nos dio reglas de mantenibilidad y, al atenderlas, nos llevó a un XSS que no marcaba. ZAP (DAST) observa la aplicación en ejecución: detectó lo que solo se ve en las respuestas reales (CSP ausente, CORS en los estáticos, atributos de cookies), cosas que el código fuente no muestra porque dependen de configuración y de librerías de terceros. Ninguno de los dos detectó los problemas más graves: el XSS almacenado en el atributo <code>onsubmit</code>, las credenciales publicadas en el login y las fallas de autorización, que solo aparecen con revisión manual y pruebas dirigidas.</p>
<p><b>Efectividad de los cambios.</b> Las tres alertas de ZAP de riesgo medio y bajo desaparecieron con el mismo recorrido; los dos hallazgos manuales de prioridad alta se confirmaron antes y se verificaron corregidos después; SonarQube cerró los 6 hallazgos heredados y los 2 nuevos con el Quality Gate aprobado, y 44 pruebas automatizadas dejan fijo el comportamiento. La CSP se probó en todas las páginas del recorrido sin violaciones.</p>
<p><b>Riesgos residuales.</b> Falta limitar intentos de login, no hay auditoría de acciones, el registro es abierto y el laboratorio usa HTTP. Un análisis pasivo no reemplaza un análisis activo ni una prueba de penetración: el informe no afirma que la aplicación esté libre de vulnerabilidades.</p>
<h3>Aporte de cada integrante</h3>
{tabla(["Integrante", "Aporte técnico"], [
    ["Xavier Romero", "Continuidad de SonarQube y correcciones de código; verificación de login y autorización con pruebas; laboratorio Docker; análisis inicial y final con ZAP; correcciones de seguridad (CSP, XSS, cookies, caché)"],
    ["Alejandro Figueroa", "Inventario de activos y mecanismos de protección; comparación de industrias; análisis de amenazas STRIDE; redacción y revisión del informe"],
])}"""


def s8():
    fuentes = [
        ("Django: autenticación de usuarios", "https://docs.djangoproject.com/en/6.1/topics/auth/default/"),
        ("Django: Content Security Policy", "https://docs.djangoproject.com/en/6.1/ref/csp/"),
        ("Django: sesiones", "https://docs.djangoproject.com/en/6.1/topics/http/sessions/"),
        ("Django: protección CSRF", "https://docs.djangoproject.com/en/6.1/ref/csrf/"),
        ("Django: almacenamiento de contraseñas", "https://docs.djangoproject.com/en/6.1/topics/auth/passwords/"),
        ("Django: checklist de despliegue", "https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/"),
        ("Django: despliegue con gunicorn", "https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/gunicorn/"),
        ("WhiteNoise: uso con Django", "https://whitenoise.readthedocs.io/en/stable/django.html"),
        ("Docker: buenas prácticas de construcción", "https://docs.docker.com/build/building/best-practices/"),
        ("Docker Compose", "https://docs.docker.com/compose/"),
        ("ZAP alerta 10038 (CSP)", "https://www.zaproxy.org/docs/alerts/10038/"),
        ("ZAP alerta 10098 (Cross-Domain)", "https://www.zaproxy.org/docs/alerts/10098/"),
        ("ZAP alerta 10010 (HttpOnly)", "https://www.zaproxy.org/docs/alerts/10010/"),
        ("ZAP alerta 10031 (atributo controlable)", "https://www.zaproxy.org/docs/alerts/10031/"),
        ("ZAP alertas 10111 y 10112", "https://www.zaproxy.org/docs/alerts/10111/"),
        ("OWASP Top 10:2025", "https://owasp.org/Top10/2025/"),
        ("OWASP XSS Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"),
        ("Microsoft: categorías STRIDE", "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats"),
        ("CWE-79, CWE-693, CWE-798, CWE-524, CWE-1004, CWE-942", "https://cwe.mitre.org/data/definitions/79.html"),
    ]
    filas = [[n, f'<a href="{u}">{u}</a>', f'<span style="white-space:nowrap">{FECHA_CONSULTA}</span>'] for n, u in fuentes]
    return f"""
<h2>8. Fuentes y anexos</h2>
{tabla(["Fuente oficial", "Enlace", "Consulta"], filas, "xs")}
<h3>Anexos (enlaces al repositorio público, rama <code>evaluacion-u3</code>)</h3>
{tabla(["Anexo", "Enlace"], [[n, f'<a href="{u}">{u.replace(REPO, "")}</a>'] for n, u in [
    ["Pull Request", PR],
    ["Reporte ZAP inicial (HTML, JSON, MD, URLs, árbol Sites)", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/zap/inicial"],
    ["Reporte ZAP final", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/zap/final"],
    ["Verificación en ZAP Desktop", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/zap/desktop"],
    ["SonarQube (métricas, issues y capturas)", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/sonarqube"],
    ["Pruebas de acceso antes y después", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/login"],
    ["Verificación manual (XSS, alerta 10031)", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/manual"],
    ["Docker (construcción, servicio, versiones)", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/docker"],
    ["Sesiones y cookies", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/evidencia/sesiones"],
    ["Herramientas reproducibles (recorrido y control de ZAP)", f"{REPO}/tree/evaluacion-u3/evaluacion_u3/herramientas"],
    ["Instrucciones del laboratorio (README)", f"{REPO}/blob/evaluacion-u3/README.md"],
]], "small")}"""


CSS = """
@page { size: A4; margin: 15mm 14mm 16mm; @bottom-center { content: counter(page); font: 9pt Arial; color: #5C6B66; } }
body { font-family: 'Liberation Sans', Arial, sans-serif; font-size: 10pt; line-height: 1.42; color: #1B2B26; }
h1 { font-size: 24pt; color: #0F3D2E; margin: 6pt 0; }
h2 { font-size: 15pt; color: #0F3D2E; border-bottom: 2px solid #9CCBB4; padding-bottom: 3pt; margin: 18pt 0 8pt; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #1F7A5A; margin: 12pt 0 5pt; page-break-after: avoid; }
p { margin: 4pt 0 7pt; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0 9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th { background: #0F3D2E; color: #fff; text-align: left; padding: 3.5pt 5pt; font-size: 9pt; }
td { border: 1px solid #D5E3DC; padding: 3pt 5pt; vertical-align: top; }
table.small td, table.small th { font-size: 8.6pt; }
table.xs td, table.xs th { font-size: 7.8pt; padding: 2.5pt 4pt; }
table.ficha td:first-child { font-weight: bold; width: 26%; background: #EEF5F1; }
table.ficha thead { display: none; }
code { font-family: 'Liberation Mono', monospace; font-size: 8.4pt; background: #F1F4F2; padding: 0 2pt; border-radius: 2pt; }
pre.code { font-family: 'Liberation Mono', monospace; font-size: 7.8pt; background: #F4F6F5; border: 1px solid #D5E3DC; border-radius: 4pt; padding: 6pt; white-space: pre-wrap; margin: 2pt 0 9pt; page-break-inside: avoid; }
.code-title { font-size: 8.5pt; font-weight: bold; color: #35607D; margin-top: 6pt; }
figure { margin: 6pt auto 10pt; text-align: center; page-break-inside: avoid; }
figure img { border: 1px solid #D5E3DC; max-height: 92mm; object-fit: contain; }
figcaption { font-size: 8.3pt; color: #5C6B66; margin-top: 3pt; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt; align-items: start; }
.grid2 figure img { max-height: 70mm; }
.good { color: #1F7A5A; font-weight: bold; } .bad { color: #B8452F; font-weight: bold; }
.pendiente { background: #FBF1E2; border-left: 0; padding: 5pt 7pt; border-radius: 4pt; }
.small { font-size: 8.6pt; }
.portada { height: 250mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always; }
.portada .kicker { color: #D9922E; font-weight: bold; letter-spacing: 1.5pt; text-transform: uppercase; font-size: 10pt; }
.portada .sub { font-size: 13pt; color: #5C6B66; margin-bottom: 18pt; }
.diagrama { width: 100%; margin: 4pt 0 8pt; } .diagrama .t { font: bold 12px Arial; text-anchor: middle; fill: #0F3D2E; }
.diagrama .s { font: 10px Arial; text-anchor: middle; fill: #5C6B66; } .diagrama .z { font: bold 11px Arial; fill: #35607D; }
"""


def main():
    cuerpo = portada() + s1() + s2() + s3() + s4() + s5() + s6() + s7() + s8()
    (AQUI / "informe.html").write_text(
        f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Informe Evaluación 3 - Desarrollo Seguro</title>'
        f'<style>{CSS}</style></head><body>{cuerpo}</body></html>')
    print("OK", AQUI / "informe.html")


if __name__ == "__main__":
    main()
