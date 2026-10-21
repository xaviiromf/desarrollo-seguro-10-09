# Entrega Evaluación U2: Desarrollo Seguro del CRUD Django

**Equipo:** Xavier Romero · Alejandro Figueroa
**Presentación:** 22-10-2026
**Proyecto:** CRUD de listas de compras, publicado en https://actividaddjango1.pythonanywhere.com
**Rama revisada:** `evaluacion-u2`, a partir de `main` (`2516b9f`)

## Contenido

| Archivo | Para qué |
|---|---|
| `Presentacion_U2_Desarrollo_Seguro.pptx` | Presentación de 15 láminas más un anexo de fuentes. Incluye el guion por persona en las notas del orador. |
| `Presentacion_U2_Desarrollo_Seguro.pdf` | Copia en PDF, exportada con LibreOffice. Las fuentes pueden variar levemente. |
| `GUION_Y_PREGUNTAS.md` | Guion, tiempos, demostración y preguntas probables con su respuesta. |
| `evidencia/` | Salidas reales de las ejecuciones. Cada archivo indica el comando, la fecha y el entorno. |

## Evidencia por criterio de la rúbrica

| Criterio | Evidencia |
|---|---|
| **2.1.2 SonarQube y OWASP** | `evidencia/sonarqube/antes_*.json`: análisis del 15-10-2026 sobre `main`. `despues_*.json`: análisis final del 19-10-2026. Las capturas del tablero están en `evidencia/capturas/` (ver más abajo). |
| **2.1.3 Validación en el servidor** | Regla en `shopping/models.py` (`QUANTITY_MIN` y `QUANTITY_MAX`). Pruebas en `shopping/tests.py`, clase `ShoppingItemValidationTests`. |
| **2.1.3 Evidencia de las pruebas** | `evidencia/tests/01_antes_validacion.txt`: 4 de 13 fallan contra el código original. `02_despues_validacion.txt`: 13 de 13 pasan. `03` y `04`: la suite completa, 25 de 25, en el entorno local y en una réplica de producción. `05_cobertura.txt`: cobertura. |
| **2.1.2 Ciclo seguro (ISO/IEC 27034)** | Commits: `feed220` (requisito y pruebas en rojo) y `1ae5774` (control implementado). Detalle en la lámina 10. |
| **2.1.2 Dependencias** | `evidencia/dependencias/01_pythonanywhere.txt`, `02_local.txt` y `03_prueba_actualizacion_django_6.1.2.txt`. |
| **2.1.2 Despliegue** | `evidencia/configuracion/00` a `05`: SECRET_KEY de producción (sin mostrar su valor), hosts aceptados antes y después, arranque sin SECRET_KEY y `check --deploy`. |
| **2.1.1 Ética** | Lámina 14 y su guion. |

## Commits de la rama `evaluacion-u2`

| Commit | Cambio |
|---|---|
| `ced924d` | Configuración de SonarQube con exclusiones técnicas |
| `feed220` | Pruebas del contrato de entrada. Fase en rojo: 4 fallan. |
| `1ae5774` | Control: cantidad entre 1 y 999 validada en el servidor |
| `cbab41a` | Corrección de la regex de `formatCLP` (javascript:S8786) |
| `11f11d0` | Eliminación de los comodines de hosts y de la SECRET_KEY por defecto |
| `d0d0ccd` | Accesibilidad: labels en los inputs (Web:InputWithoutLabelCheck) |
| `f29535c` | Versiones exactas en `requirements.txt`, con Django 6.1.2 |
| `37295d1` | Subtotal en formato CLP en el mensaje de producto agregado |
| `019c866` | `Number.parseFloat` (javascript:S7773, confiabilidad) |

Los demás commits son configuración de cobertura y archivos de evidencia.

## Capturas incluidas en `evidencia/capturas/`

| Archivo | Muestra |
|---|---|
| `sonarqube_01_resumen.png` | Quality Gate aprobado; Security, Reliability y Maintainability en A; cobertura 64,7 % |
| `sonarqube_02_actividad.png` | Historial de análisis, del 15-10 al 20-10 |
| `sonarqube_03_obs1_S8786.png` | Observación 1 en estado Closed (Fixed) |
| `sonarqube_04_obs2_S1192.png` | Observación 2 en estado Closed (Fixed) |
| `pythonanywhere_01_vencimiento_antes.png` | La app iba a deshabilitarse el 24-10-2026 |
| `pythonanywhere_02_vencimiento_renovado.png` | Renovada: vence el 21-11-2026 |
| `pythonanywhere_03_force_https.png` | Force HTTPS activado |
| `01_antes_validacion.png`, `02_despues_validacion.png`, `01_antes_hosts.png`, `03_despues_hosts_env_recomendado.png` | Salidas de pruebas y de configuración, generadas a partir de los `.txt` |

## Cambios aplicados en PythonAnywhere (20-10-2026)

1. **`.env`:**
   - SECRET_KEY nueva, de 50 caracteres aleatorios.
   - `ALLOWED_HOSTS=actividaddjango1.pythonanywhere.com`.
   - `CSRF_TRUSTED_ORIGINS=https://actividaddjango1.pythonanywhere.com`, con el typo corregido.
2. **Rama desplegada:** `evaluacion-u2`, mediante `git bundle`, porque el servidor no tiene credenciales de GitHub. Se instaló `requirements.txt` (Django 6.1.1 → 6.1.2) y se ejecutaron `migrate` y `collectstatic`.
3. **Web app:** Force HTTPS activado, recarga, y renovación hasta el 21-11-2026.
4. **Verificación en vivo:**
   - HTTP redirige a HTTPS.
   - El login funciona.
   - Cantidad 0 se rechaza y cantidad 5 se acepta.
   - La prueba usó un usuario ficticio que se borró al terminar.

   Evidencia en `evidencia/configuracion/06` a `08`.

## Mantenimiento

- **Renovar la app cada mes:** pestaña **Web** → **Run until 1 month from today**. PythonAnywhere envía un correo de aviso una semana antes.
- **SonarQube:** se inicia con `~/tools/start-sonarqube.sh` y se usa en http://localhost:9000.
  - Para escanear: `SONAR_TOKEN=<token> sonar-scanner` desde la raíz del proyecto.
  - El token usado durante la revisión ("claude code") se revocó el 20-10. Sigue vigente tu token "desarrollo-seguro-django" del 15-10; si no lo tienes guardado, crea uno nuevo en *My Account → Security*.
- **PythonAnywhere:** el token de API usado para el despliegue se revocó el 20-10. La cuenta quedó con un token nuevo que nadie ha usado; puedes ignorarlo.
- **Reconstruir la presentación:** el generador está en `fuente_presentacion/build.js` (requiere `pptxgenjs`).
