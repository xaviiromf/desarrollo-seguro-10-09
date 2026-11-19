# Plan: Evaluación 3 — CRUD Django con login, Docker y OWASP ZAP

Fuente: `Evaluacion_3_Desarrollo_Seguro.pdf` (6 páginas, 80 puntos). Entrega: **un informe técnico en PDF**, de 10 a 15 páginas de cuerpo, con capturas legibles.

## 1. Qué pide la guía (resumen)

| Etapa | Qué hay que hacer | Puntos |
|---|---|---|
| 1. SonarQube | Recuperar los hallazgos de la Evaluación 2; regla, archivo, prioridad y decisión; código antes/después vinculado a commit o PR | 10 |
| 2. Login y acceso | Login correcto e incorrecto, logout por POST con CSRF, rutas privadas bloqueadas en el servidor, permisos por usuario al consultar, crear, editar y eliminar | 15 |
| 3. Datos y sesiones | Inventario de al menos 4 activos (uno personal y uno del negocio), mecanismos de protección y sus límites, el mismo dato comparado en 2 industrias, backend de sesiones y cookies | 15 |
| 4. Docker | Dockerfile (imagen oficial de Python), `compose.yaml` con el puerto solo en `127.0.0.1:8000`, perfil de laboratorio (DEBUG=False, ALLOWED_HOSTS acotado, secretos por variables), `.dockerignore`, `.gitignore`, `.env.example`, README reproducible, versiones, capturas y diagrama | 10 |
| 5. ZAP inicial | Sesión y contexto de ZAP, exploración manual con cuenta de prueba, reporte inicial (legible y JSON o MD), tabla de hallazgos con origen y decisión, 3 amenazas STRIDE | 15 |
| 6. Correcciones | Corregir lo confirmado, reconstruir el contenedor, segundo análisis comparable en una sesión nueva, relacionar cada hallazgo con su cambio, prueba y resultado | 10 |
| 7. Informe | PDF en 8 secciones: SAST frente a DAST, riesgos residuales, aporte de cada integrante, fuentes con fecha y enlaces a repositorio, PR y reportes | 5 |

**Reglas que cruzan todo el trabajo:**
- Solo laboratorio local, con datos y cuentas ficticias.
- **No escanear PythonAnywhere** ni sitios de terceros.
- Ningún `.env`, clave, token ni base de datos real en el repositorio o en las capturas.
- ZAP debe analizar **la app dentro de Docker**, no un `runserver` en el equipo.
- No inventar hallazgos, no ocultarlos con exclusiones y no atribuir alertas de terceros al CRUD.
- Se exige un **Pull Request descriptivo**.

## 2. Punto de partida (lo que ya tenemos)

| Ya hecho | Dónde |
|---|---|
| Login, logout y registro con vistas de Django | `shopping/views.py` (UserLoginView, UserLogoutView, UserRegisterView) |
| Logout por **POST** con `{% csrf_token %}` | `templates/base.html:45` |
| Vistas privadas protegidas (14 usos de `LoginRequiredMixin`) | `shopping/views.py` |
| Aislamiento por usuario en el servidor (`get_queryset` y `get_object_or_404(..., user=...)`) | `shopping/views.py` |
| Pruebas de aislamiento: lista, detalle y CSV de otro usuario dan 404 | `shopping/tests.py` |
| Validación de cantidad (1 a 999) en el servidor, con 13 pruebas | Evaluación 2 |
| SonarQube: Quality Gate aprobado, 0 vulnerabilidades, 0 hotspots, **6 code smells pendientes** | `evaluacion_u2/evidencia/sonarqube/` |
| Django 6.1.2 con versiones fijas; configuración por variables de entorno | `requirements.txt`, `settings.py` |

**Lo que falta o hay que verificar:**
- **Docker:** no existe ningún archivo todavía.
- **Pruebas de permisos incompletas:** faltan las de escritura sobre datos ajenos (editar, eliminar, marcar o duplicar una lista o un producto de otro usuario) y las de un anónimo haciendo POST directo.
- **Cabeceras de seguridad:** no hay CSP ni `Cache-Control` en páginas privadas; hay que revisar cómo quedan las cookies en el perfil de laboratorio.
- **Registro abierto:** cualquiera puede crear una cuenta. Hay que decidir y justificar si se mantiene.
- **En el equipo:** ZAP no está instalado y el usuario no está en el grupo `docker`.

## 3. Plan de trabajo por etapa

Trabajaremos en una rama nueva, `evaluacion-u3`. Cada etapa se cierra con commits propios y, al final, con un **Pull Request** hacia `main`. La evidencia se guarda en `evaluacion_u3/evidencia/<etapa>/`.

### Etapa 0. Preparar el equipo (antes de empezar)
1. **Agregar tu usuario al grupo docker** (lo haces tú, requiere contraseña): `sudo usermod -aG docker $USER` y luego cerrar sesión y volver a entrar.
2. **Instalar OWASP ZAP Desktop** en el equipo anfitrión. Necesita Java 17 o superior, y ya tenemos un JDK 21 en `~/tools`.
3. **Definir la fecha de entrega** y el reparto de tareas entre Xavier y Alejandro.

### Etapa 1. Continuidad de SonarQube (10 pts)
- Usar como línea base la evidencia de la Evaluación 2 (`antes_*.json` y `despues_*.json`, con sus capturas).
- **Atender los 6 code smells pendientes**, con regla, archivo, prioridad y decisión para cada uno:
  - `python:S1192` en `views.py`: rutas repetidas; corregir con constantes.
  - `python:S1481`: variable sin uso; corregir.
  - `javascript:S3776`: función JS demasiado compleja; refactorizar o conservar con fundamento.
  - `javascript:S2486`: `catch` vacío; corregir con manejo de error.
  - `javascript:S6582`: optional chaining; corregir.
- Mostrar el código antes y después, re-escanear y vincular cada corrección con su commit.
- Explicar que un hotspot exige revisión, pero no confirma por sí solo una vulnerabilidad (hoy tenemos 0).

### Etapa 2. Login y autorización (15 pts)
- Revisar lo existente contra los tres requisitos de la guía y documentarlo.
- **Pruebas nuevas:**
  - Login válido, login inválido (credenciales incorrectas) y logout por POST.
  - **Logout por GET rechazado** (405) y **POST sin token CSRF rechazado** (403).
  - Un anónimo que entra por URL directa a una ruta privada es redirigido al login.
  - Un anónimo que hace POST de escritura no logra cambiar nada.
  - Un usuario que intenta editar, eliminar, marcar o duplicar datos de otro recibe 404 y no cambia nada.
- **Definir la matriz de acceso:** qué puede hacer el dueño de una lista, otro usuario, un anónimo y el administrador.
- **Evidencia:** capturas del login correcto e incorrecto, una petición directa a una ruta protegida con `curl` y la salida de las pruebas.
- **Decisión sobre el registro abierto:** mantenerlo y justificarlo, o restringirlo.

### Etapa 3. Datos sensibles, sesiones e industrias (15 pts)
- **Inventario de activos** (al menos 4):
  - Cuenta de usuario: nombre de usuario y correo (dato personal).
  - Contraseña, guardada como hash PBKDF2.
  - Listas y productos con presupuestos e historial de compras (registro del negocio).
  - Sesión: la cookie `sessionid` y la tabla `django_session`.
  - Exportación CSV y panel de administración.
- **Mecanismos de protección:** para cada uno, su propósito y su límite.
  - Minimización: el correo es opcional.
  - Autorización: filtro por usuario en el servidor.
  - Hash de contraseñas.
  - Enmascaramiento: por ejemplo, en el admin, con el límite de que la exportación CSV igual revela el valor.
  - Cifrado: explicar por qué no se justifica en este caso.
- **Comparación de dos industrias:** el mismo dato, el historial de compras, en **comercio minorista** y en **salud o farmacia**, donde las compras revelan condiciones médicas.
- **Sesiones y cookies:**
  - El backend es `django.contrib.sessions.backends.db`, que guarda la sesión en la tabla `django_session`.
  - Revisar los atributos de las cookies `sessionid` y `csrftoken`: HttpOnly, Secure y SameSite.
  - Explicar la diferencia entre el perfil de laboratorio (HTTP) y producción (HTTPS).

### Etapa 4. Docker (10 pts)
- **`Dockerfile`:**
  - Imagen oficial `python:3.12-slim`, la misma serie que PythonAnywhere.
  - Instala desde `requirements.txt`.
  - Corre con un usuario sin privilegios (no root).
  - Ejecuta `collectstatic`.
- **`compose.yaml`:**
  - Servicio `web` con el puerto `127.0.0.1:8000:8000` (solo la interfaz local).
  - Archivo de variables del perfil de laboratorio.
  - Volumen para la base SQLite de laboratorio.
  - Healthcheck.
- **Perfil de laboratorio:**
  - `DEBUG=False`.
  - `ALLOWED_HOSTS=127.0.0.1,localhost`.
  - Secretos por variables de entorno.
  - Cookies `Secure` desactivadas solo porque el laboratorio usa HTTP, documentado como riesgo contextual.
- **Archivos de apoyo:**
  - `.dockerignore` y `.gitignore`: excluir venv, `.env`, bases de datos y archivos ajenos.
  - `.env.example` sin secretos.
  - `README.md` con requisitos, construcción, arranque, migraciones, cuentas de prueba, URL y pruebas.
- **Servidor web de la imagen:** con DEBUG=False, `runserver` no sirve los estáticos. Propuesta: **gunicorn más WhiteNoise**, siguiendo el ejemplo del docente para los estáticos (ver sección 4).
- **Evidencia:**
  - Versiones de Python, Django, Docker Compose y ZAP.
  - Capturas de la construcción, de `docker compose ps` y de la app abierta en `http://127.0.0.1:8000`.
  - Diagrama: navegador → ZAP (proxy en el equipo) → `127.0.0.1:8000` → contenedor web → SQLite en un volumen.

### Etapa 5. ZAP inicial (15 pts)
- **Sesión y contexto:** sesión nueva y contexto limitado a `http://127.0.0.1:8000.*`. Registrar la URL, la fecha y la versión de la imagen o el commit.
- **Recorrido:** exploración manual con el navegador de ZAP y una cuenta de prueba. Recorrer login, listas, productos, CSV y logout, y esperar a que termine el análisis pasivo.
- **Reporte inicial:** HTML legible más JSON o MD, filtrado al objetivo.
- **Tabla de hallazgos**, agrupada por regla y causa, con estas columnas:
  - ID propio, regla de ZAP, riesgo y confianza.
  - URL, método y parámetro o cabecera.
  - Petición y respuesta, sin secretos.
  - Origen: aplicación propia, infraestructura o tercero.
  - Decisión, impacto, prioridad y CWE (solo si ZAP lo entrega).
- **3 amenazas STRIDE como mínimo**, por ejemplo:
  - Suplantación: fuerza bruta en el login.
  - Divulgación de información: la exportación CSV de otro usuario.
  - Elevación de privilegios: el panel de administración.
- **Hallazgos probables, a confirmar:** falta de CSP, falta de Permissions-Policy, cookies sin `Secure` en HTTP, la cabecera `Server` y caché de páginas privadas.

### Etapa 6. Correcciones y verificación final (10 pts)
- **Corregir lo que se confirme**, priorizado por impacto. Candidatos:
  - **CSP** con la configuración nativa de Django 6 (`SECURE_CSP` y su middleware), sin dependencias nuevas, ajustada a los recursos reales y probada.
  - `Cache-Control: no-store` en vistas privadas.
  - Cabecera Permissions-Policy.
  - Ajustes de cookies.
- **Verificación:**
  - Reconstruir el contenedor.
  - Re-ejecutar las pruebas.
  - Segundo análisis de ZAP en una **sesión nueva**, con el mismo alcance y la misma cuenta.
- **Tabla final:** cada hallazgo con su cambio, commit o PR, prueba y estado (resuelto, mitigado, pendiente, falso positivo o contextual). Una alerta que desaparece porque no se visitó la ruta no cuenta como corregida.

### Etapa 7. Informe PDF (5 pts)
- **Las 8 secciones de la guía:**
  1. Identificación.
  2. SonarQube y login.
  3. Datos y sesiones.
  4. Docker.
  5. ZAP inicial.
  6. Correcciones.
  7. Conclusiones: SAST frente a DAST, riesgos residuales y aporte de cada integrante.
  8. Fuentes y anexos.
- Fuentes oficiales con fecha de consulta y enlaces al repositorio, al PR y a los reportes completos.

## 4. Material de apoyo del docente (`ejemplos-docker`)
Son dos ejemplos casi idénticos de un CRUD de tareas con login. Revisé que lo que reportó el agente coincide con los archivos.

| Ejemplo | Qué muestra |
|---|---|
| `ej-actividad/` | Django 5.2 con SQLite en un **volumen** (`/data`), WhiteNoise para los estáticos, `env_file: .env` y puerto `127.0.0.1:8000:8000` |
| `ej-db/` | La misma app con **PostgreSQL 17** como servicio aparte, con healthcheck (`pg_isready`), `depends_on: service_healthy` y la base **sin publicar** al host |

**Lo que vamos a reutilizar:**
- **La estructura del `Dockerfile`:** `python:*-slim`, `PYTHONDONTWRITEBYTECODE` y `PYTHONUNBUFFERED`, copiar `requirements.txt` antes del código para aprovechar la caché, y `pip --no-cache-dir`.
- **El `compose.yaml` de `ej-actividad`:** puerto solo en `127.0.0.1`, volumen con nombre para SQLite, `env_file` y variables específicas de Docker para el perfil de laboratorio.
- **El `.dockerignore`:** `.env`, `.env.*`, `*.sqlite3*`, `staticfiles/`, `.git/` y `__pycache__`. Le agregamos `venv/`, `node_modules/` y `evaluacion_u*/`.
- **WhiteNoise** para servir los estáticos con `DEBUG=False`. Es el mismo enfoque del docente. Nuestro CSS de Tailwind ya está compilado en el repositorio, así que **no hace falta Node** dentro de la imagen.
- **La ruta de SQLite por variable** (`SQLITE_PATH=/data/db.sqlite3`). Lo resolvemos con nuestro `DATABASE_URL` actual, sin cambiar `settings.py`.
- **Los interruptores de cookies Secure y SSL por variable.** Desactivados solo en el laboratorio HTTP, como indica el README del docente.

**Lo que mejoramos respecto del ejemplo** (los ejemplos no lo traen; son debilidades que conviene corregir y documentar):
- **Usuario sin privilegios** (`USER`) en el Dockerfile. El ejemplo corre como root.
- **gunicorn** en vez de `runserver`, que es un servidor de desarrollo.
- **Healthcheck** del servicio `web` y política `restart`.
- **Versiones fijas** en `requirements.txt` (ya las tenemos). El ejemplo usa rangos.
- **Imagen base `python:3.12-slim`**, la misma serie que PythonAnywhere. El ejemplo usa 3.13.
- **Migraciones fuera del `CMD`** (o justificadas solo para el laboratorio). El ejemplo las ejecuta en cada arranque.
- **Validadores de contraseña:** los ejemplos no los tienen; nosotros ya los tenemos.

**SQLite o PostgreSQL:** usamos **SQLite en un volumen**. Es lo que ya usa el proyecto y lo que muestra `ej-actividad`. Pasar a PostgreSQL agrega un servicio y una dependencia (`psycopg`) que la guía no exige; queda como mejora opcional.

**Advertencia:** los `.env` de los ejemplos traen una SECRET_KEY y una contraseña de PostgreSQL reales. **No hay que copiarlos**: generamos los nuestros a partir de `.env.example`.

## 5. Decisiones
- **Fecha de entrega: 19-11-2026.**
- **Reparto aprobado:** Xavier se encarga de SonarQube, login, Docker, ZAP y correcciones. Alejandro, del inventario de activos, la comparación de industrias, STRIDE y la redacción del informe.
- **Equipo listo:** el usuario está en el grupo docker y OWASP ZAP 2.17.0 está instalado en `~/tools` (se abre con `~/tools/zap.sh`).
- **Pendientes:** registro abierto, y gunicorn más WhiteNoise.
