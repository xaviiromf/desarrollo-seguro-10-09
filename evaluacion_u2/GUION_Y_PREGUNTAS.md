# Guion, demostración y preguntas probables

El guion completo de cada lámina está en las **notas del orador** del PPTX. Este documento resume lo que hay que memorizar.

## Reparto y tiempos (objetivo: 9 a 9,5 minutos)

| Lámina | Tema | Expone | Tiempo |
|---|---|---|---|
| 1 | Portada | Xavier | 0:10 |
| 2 | Qué revisamos y cómo | Xavier | 0:35 |
| 3 | SonarQube: lo que midió y lo que no | Xavier | 0:50 |
| 4 | Observación 1 (regex, S8786) | Xavier | 0:40 |
| 5 | Observación 2 (comodín, S1192) | Xavier | 0:50 |
| 6 | OWASP A02 y A06 | Xavier | 0:40 |
| 7 | Contrato de entrada | Xavier | 0:35 |
| 8 | Mejora: antes y después | Xavier | 0:35 |
| 9 | Seis casos y demostración | Xavier | 1:10 |
| 10 | Trazabilidad e ISO/IEC 27034 | Xavier | 0:40 |
| 11 | Python y dependencias | Alejandro | 0:40 |
| 12 | Recomendaciones de despliegue | Alejandro | 0:40 |
| 13 | Limitación de PythonAnywhere | Alejandro | 0:30 |
| 14 | Ética y concientización | Alejandro | 0:45 |
| 15 | Conclusión | Alejandro y Xavier | 0:30 |

La lámina 16 (fuentes) es un anexo y no se expone.

## Las 5 frases que no pueden faltar

1. "El Quality Gate aprobado no significa que la aplicación sea segura: SonarQube no detectó la clave débil ni la falta de rango en la cantidad."
2. "Una alerta de mantenibilidad no es automáticamente una vulnerabilidad: la regex solo recibe dígitos en el navegador del propio usuario."
3. "La restricción del HTML no es validación: probamos con POST directo a la vista, sin navegador."
4. "Primero escribimos las pruebas y fallaron 4 de 13 con el código original; ese es nuestro antes real."
5. "Aplicamos el enfoque de ISO/IEC 27034; no decimos que el proyecto esté certificado."

## Demostración en vivo (lámina 9, Xavier, unos 20 segundos)

Prepárala antes de empezar: deja una terminal abierta en la raíz del proyecto, con el venv activo y la letra grande.

```bash
python manage.py test shopping.tests.ShoppingItemValidationTests.test_backend_crear_con_cantidad_cero_no_guarda -v 2
```

Qué decir mientras corre: *"Esta prueba hace un POST directo a la vista de crear producto con cantidad 0. No pasa por el navegador. Comprueba que no se guarda nada y que el usuario recibe el mensaje de error."*

Resultado esperado: `... ok` y `OK`.

Plan B si algo falla: mostrar `evidencia/capturas/02_despues_validacion.png`.

## Checklist del día de la presentación

- [ ] PythonAnywhere: el sitio responde y la app está renovada (pestaña Web, **Run until 1 month from today**).
- [ ] Capturas de SonarQube tomadas (lista en `README.md`).
- [ ] La terminal de la demostración está lista, con el venv activo, y la prueba se ejecutó una vez antes.
- [ ] El PPTX se abre en el computador de la sala, con la vista del moderador para ver las notas.
- [ ] Ninguna captura ni lámina muestra el valor de la SECRET_KEY ni el contenido del `.env`.

## Preguntas probables

### Para Xavier

**¿Por qué validar en el modelo y no solo en el formulario?**
Porque el modelo es el punto común. Así el mismo control aplica al crear, al editar y en el admin de Django. El ModelForm ejecuta esos validadores en `is_valid()` mediante `full_clean()`.

**¿Por qué 999 como máximo?**
Es una regla de negocio que definimos para una lista de compras doméstica: ninguna compra real necesita mil unidades de un producto. Además evita totales absurdos en el presupuesto. Está en constantes (`QUANTITY_MIN` y `QUANTITY_MAX`), así que cambiarla es una línea, y las pruebas de frontera la verifican.

**¿Qué pasa con los productos que ya estaban guardados fuera de rango?**
Los validadores no modifican datos existentes: se aplican cuando alguien crea o edita. La migración 0004 no cambia la base de datos. Revisar los registros existentes en producción quedó pendiente; no lo verificamos.

**¿Por qué las pruebas del precio pasaban antes?**
Porque ese control ya era correcto: `PositiveIntegerField` rechaza los negativos y el `clean()` del formulario maneja el caso "sin precio". La pauta pide no alterar un control correcto, así que lo verificamos con pruebas nuevas en vez de cambiarlo.

**¿La cobertura de SonarQube (64,7 %) no coincide con coverage.py (82 %)?**
Miden distinto. SonarQube combina líneas y condiciones y considera todos los archivos Python del alcance. coverage.py reporta solo líneas, sobre los archivos configurados. Ninguna de las dos cifras prueba que el sistema sea seguro.

**¿Por qué SonarQube no marcó la SECRET_KEY?**
En nuestra instalación ninguna regla la reportó. Eso muestra justamente el límite de la herramienta. La encontramos con `check --deploy` (aviso W009) y comparando hashes con el `.env.example`.

**¿Por qué el comodín es un problema si igual hay token CSRF?**
El token sigue protegiendo, pero el comodín debilita dos defensas adicionales. La validación del encabezado Host aceptaría subdominios de otros usuarios. La verificación de origen CSRF confiaría en sitios que no controlamos. Además ocultaba errores reales del `.env`.

**¿Qué es un ASC en ISO/IEC 27034?**
Un control de seguridad de la aplicación junto con su forma de verificarlo. En nuestro caso, el control es el validador y la medición de verificación son las pruebas, que dejan evidencia.

**¿Diferencia entre A02 y A06?**
A02 es configuración incorrecta: el código puede estar bien, pero el despliegue no. A06 es diseño inseguro: faltaba definir la regla, y por eso faltaba el control.

### Para Alejandro

**¿Por qué no actualizaron Django en producción?**
La pauta no lo exige, y un cambio en producción se coordina. Antes de recomendarlo verificamos lo necesario: misma serie (6.1.1 a 6.1.2), notas de seguridad y las 25 pruebas pasando con 6.1.2. Es el siguiente paso recomendado.

**¿Por qué local usa Django 5.2 y producción 6.1?**
Porque `requirements.txt` dice `Django>=5.0.0`, y cada entorno instaló una versión distinta. Por eso recomendamos fijar versiones exactas. Lo relacionamos con A03, fallas en la cadena de suministro.

**¿Si el repositorio es privado, la clave igual es un riesgo?**
Sí. La puede ver cualquier persona con acceso al repositorio, a una copia o a un respaldo, y además es débil según Django. Un secreto que estuvo en git se considera expuesto: se rota.

**¿Qué pasa al rotar la SECRET_KEY?**
Se cierran las sesiones activas y dejan de valer los enlaces firmados pendientes, como los de restablecer contraseña. Para este CRUD es aceptable.

**¿La limitación de PythonAnywhere es una falla de seguridad?**
No. Es una restricción del plan gratuito: la app vence al mes si no se renueva. Afecta la disponibilidad del CRUD, no su seguridad.

**¿Qué harían si encuentran una falla en la app de otro usuario?**
No explotarla. Avisar al dueño o a PythonAnywhere de forma responsable y sin acceder a sus datos.

**¿Cómo saben que la acción de concientización sirve?**
Es concreta y medible: un checklist publicado en el README y una charla de 10 minutos. Se puede verificar si en los siguientes push aparecen secretos o falla `check --deploy`.
