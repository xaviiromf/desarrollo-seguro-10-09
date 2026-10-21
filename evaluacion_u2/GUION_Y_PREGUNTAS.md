# Guion, demostración y preguntas probables

El guion completo de cada lámina está en las **notas del orador** del PPTX. Este documento resume lo que hay que memorizar.

## Reparto y tiempos (objetivo: 8,5 a 9 minutos)

El guion de las notas suma unas 1.160 palabras. A ritmo normal (150 palabras por minuto) son unos 7,8 minutos, más 20 segundos de demostración y las transiciones.

| Lámina | Tema | Expone | Tiempo |
|---|---|---|---|
| 1 | Portada | Xavier | 0:10 |
| 2 | Qué revisamos y cómo | Xavier | 0:25 |
| 3 | SonarQube: lo que midió y lo que no | Xavier | 0:40 |
| 4 | Observación 1 (regex, S8786) | Xavier | 0:35 |
| 5 | Observación 2 (comodín, S1192) | Xavier | 0:40 |
| 6 | OWASP A02 y A06 | Xavier | 0:30 |
| 7 | Contrato de entrada | Xavier | 0:30 |
| 8 | Mejora: antes y después | Xavier | 0:25 |
| 9 | Seis casos y demostración | Xavier | 1:00 |
| 10 | Trazabilidad e ISO/IEC 27034 | Xavier | 0:35 |
| 11 | Python y dependencias | Alejandro | 0:45 |
| 12 | Recomendaciones de despliegue | Alejandro | 0:40 |
| 13 | Limitación de PythonAnywhere | Alejandro | 0:30 |
| 14 | Ética y concientización | Alejandro | 0:45 |
| 15 | Conclusión | Alejandro y Xavier | 0:25 |

**Total: unos 8:35.** La lámina 16 (fuentes) es un anexo y no se expone. Las líneas "Fuente (no leer)" de las notas no se dicen en voz alta: están ahí porque la pauta pide las fuentes en las notas.

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

Primero aparecen líneas `Applying ...` de la base de prueba; es normal. Al final debe decir `... ok` y `OK`.

Plan B si algo falla: mostrar `evidencia/capturas/02_despues_validacion.png`.

## Checklist del día de la presentación

- [ ] PythonAnywhere: el sitio responde. La app ya está renovada hasta el 21-11-2026.
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
Los validadores no modifican datos existentes: se aplican cuando alguien crea o edita. La migración 0004 no cambia la base de datos. Lo verificamos en producción el 20-10: de 15 productos guardados, ninguno estaba fuera de rango.

**¿Por qué las pruebas del precio pasaban antes?**
Porque ese control ya era correcto: `PositiveIntegerField` rechaza los negativos y el `clean()` del formulario maneja el caso "sin precio". La pauta pide no alterar un control correcto, así que lo verificamos con pruebas nuevas en vez de cambiarlo.

**¿Por qué quedan 6 code smells?**
Son de mantenibilidad: literales repetidos en las vistas, una función JavaScript compleja, un `catch` vacío y una variable sin uso. No afectan la seguridad, así que los dejamos como mejora pendiente con fundamento, que es una de las decisiones que permite la pauta.

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

**¿Por qué actualizaron Django si la pauta no lo exige?**
Porque 6.1.2 corrige cuatro CVE y era un cambio de bajo riesgo. Antes de actualizar revisamos lo que pide la pauta: misma serie (6.1.1 a 6.1.2), notas de seguridad y las 25 pruebas pasando con 6.1.2 en Python 3.12 y 3.14. Lo aplicamos el 20-10 y verificamos el sitio en vivo.

**¿Por qué local usaba Django 5.2 y producción 6.1?**
Porque `requirements.txt` decía `Django>=5.0.0`, y cada entorno instaló una versión distinta. Fijamos versiones exactas (commit `f29535c`) y ahora los dos usan 6.1.2. Lo relacionamos con A03, fallas en la cadena de suministro.

**¿Si el repositorio es privado, la clave igual es un riesgo?**
Sí. La puede ver cualquier persona con acceso al repositorio, a una copia o a un respaldo, y además es débil según Django. Un secreto que estuvo en git se considera expuesto: se rota.

**¿Qué pasa al rotar la SECRET_KEY?**
Se cierran las sesiones activas y dejan de valer los enlaces firmados pendientes, como los de restablecer contraseña. Para este CRUD es aceptable.

**¿La limitación de PythonAnywhere es una falla de seguridad?**
No. Es una restricción del plan gratuito: la app vence al mes si no se renueva. Afecta la disponibilidad del CRUD, no su seguridad.

**¿Qué harían si encuentran una falla en la app de otro usuario?**
No explotarla. Avisar al dueño o a PythonAnywhere de forma responsable y sin acceder a sus datos.

**¿Cómo saben que la acción de concientización sirve?**
Es concreta y medible. El checklist ya está publicado en el `README.md` del repositorio y se suma una charla de 10 minutos. Se puede verificar si en los siguientes push aparecen secretos o falla `check --deploy`.

**¿Probaron en producción? ¿No dice la pauta que se use una copia local?**
Las pruebas de validación se hicieron en copia local. En producción solo verificamos, después de desplegar, que nuestra propia app funcionara. Usamos un usuario ficticio que borramos al terminar y nunca tocamos datos reales ni apps de otros.
