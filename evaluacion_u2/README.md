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

Los demás commits son configuración de cobertura y archivos de evidencia.

## Capturas que debe tomar Xavier

SonarQube exige iniciar sesión en el navegador, así que estas capturas no se pueden automatizar. Guárdalas en `evidencia/capturas/` con estos nombres:

1. `sonarqube_01_resumen.png`: http://localhost:9000/dashboard?id=desarrollo-seguro-django (Quality Gate y métricas).
2. `sonarqube_02_actividad.png`: pestaña **Activity** del proyecto, que muestra los dos análisis.
3. `sonarqube_03_obs1_S8786.png`: **Issues** → filtro *Status: Closed* → issue `javascript:S8786` en `calculator.js`.
4. `sonarqube_04_obs2_S1192.png`: el mismo filtro → issue `python:S1192` en `settings.py`.
5. `pythonanywhere_vencimiento.png`: pestaña **Web** de PythonAnywhere, con la fecha en que se deshabilitará el sitio.

Para levantar SonarQube: `~/tools/start-sonarqube.sh`. Espera alrededor de un minuto antes de abrir http://localhost:9000.

`evidencia/capturas/` ya incluye imágenes de las salidas de pruebas y de configuración, generadas a partir de los `.txt`.

## Pasos pendientes en PythonAnywhere, en este orden

**Importante:** sin el paso 2, el sitio dará Error 400 al desplegar esta rama.

1. Genera una SECRET_KEY nueva en la consola de PythonAnywhere:
   `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"`
2. Edita `~/desarrollo-seguro-10-09/.env` y deja estas tres líneas:
   - `SECRET_KEY=<la clave nueva>`
   - `ALLOWED_HOSTS=actividaddjango1.pythonanywhere.com`
   - `CSRF_TRUSTED_ORIGINS=https://actividaddjango1.pythonanywhere.com`
3. Despliega la rama, desde el virtualenv activo y dentro de la carpeta del proyecto:
   ```bash
   git fetch && git checkout evaluacion-u2
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
4. En la pestaña **Web**, pulsa **Reload** y luego **Run until 1 month from today**.
5. Opcional, recomendado en la lámina 11: `pip install Django==6.1.2`, otra vez **Reload**, y prueba el sitio.
