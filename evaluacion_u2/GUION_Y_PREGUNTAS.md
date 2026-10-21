# Guion de la presentación y preparación

Lo que dice cada uno está también en las **notas del orador** del PPTX, así que se puede seguir en el modo presentador. La idea no es leerlo palabra por palabra, sino decirlo con sus propias palabras.

**Regla general:** en las láminas se ven los términos técnicos (nombres de reglas, código, archivos), pero al hablar **no los nombramos**: explicamos la idea en palabras simples. Si el profesor pregunta por un término, ahí sí lo explicamos.

## 1. Antes de empezar: qué tener preparado

### Días antes
- [ ] Hacer al menos **dos ensayos juntos, con cronómetro**. La meta es terminar entre 8:30 y 9:30.
- [ ] Alejandro abre los enlaces de las fuentes de sus láminas (11 a 13) para conocerlos: la pauta pide no limitarse a copiar a una IA.
- [ ] Los dos leen las preguntas probables (sección 4) y hacen un simulacro: uno pregunta y el otro responde.
- [ ] Entregar el ZIP en la plataforma del curso.

### El día de la presentación (30 minutos antes)
**Notebook de Xavier:**
- [ ] Cargador conectado y adaptador HDMI o USB-C a mano.
- [ ] Notificaciones silenciadas (modo no molestar) y programas innecesarios cerrados.
- [ ] Pantalla en modo **extendido**, no duplicado, para ver las notas en el modo presentador.
- [ ] El PPTX abierto en **PowerPoint**, no el PDF, y probado una vez en modo presentador.

**Terminal para la demostración**, abierta y probada:
```bash
cd ~/Projects/desarrollo-seguro/10-09/django-project
source venv/bin/activate
python manage.py test shopping.tests.ShoppingItemValidationTests.test_backend_crear_con_cantidad_cero_no_guarda -v 2
```
- [ ] Ejecutar el comando una vez antes de empezar, para confirmar que termina en `OK`.
- [ ] Limpiar la pantalla (`clear`) y dejar el comando listo con la flecha hacia arriba.
- [ ] Letra grande en la terminal (Ctrl + Shift + +) para que se lea desde el fondo de la sala.

**Navegador:**
- [ ] Una pestaña abierta en https://actividaddjango1.pythonanywhere.com, para comprobar que responde y por si piden verla.
- [ ] Opcional, por si preguntan por SonarQube: levantarlo con `~/tools/start-sonarqube.sh`, esperar un minuto e iniciar sesión en http://localhost:9000.

**Plan B:** dejar abierta la imagen `evaluacion_u2/evidencia/capturas/02_despues_validacion.png` por si la demostración falla.

**Respaldo:** llevar el PPTX y el ZIP también en un pendrive.

### Qué NO mostrar nunca en pantalla
- El archivo `.env`, ni local ni de PythonAnywhere, ni ninguna clave secreta.
- La consola de PythonAnywhere, porque su historial puede tener datos sensibles.

### Roles durante la presentación
- **Xavier:** controla el notebook, expone las láminas 1 a 10 y hace la demostración.
- **Alejandro:** expone las láminas 11 a 14 y comparte la 15. Pide a Xavier que avance las láminas, o usa un control remoto si hay.
- **En las preguntas:** responde quien expuso ese tema. Si no saben algo, decirlo con honestidad: «No lo verificamos; lo podemos revisar».

## 2. Reparto y tiempos

El texto hablado suma unas 1325 palabras: unos 8.8 minutos a ritmo normal, más la demostración y las transiciones.

| Lámina | Tema | Expone | Tiempo |
|---|---|---|---|
| 1 | Portada | Xavier | 0:15 |
| 2 | Qué revisamos y cómo lo hicimos | Xavier | 0:25 |
| 3 | SonarQube: lo que midió y lo que no | Xavier | 0:45 |
| 4 | Observación 1 | Xavier | 0:35 |
| 5 | Observación 2 | Xavier | 0:40 |
| 6 | OWASP Top 10:2025 | Xavier | 0:30 |
| 7 | Reglas de los dos datos | Xavier | 0:30 |
| 8 | La mejora: antes y después | Xavier | 0:25 |
| 9 | Casos ejecutados y demostración | Xavier | 1:00 |
| 10 | Trazabilidad e ISO/IEC 27034 | Xavier | 0:40 |
| 11 | Python y dependencias | Alejandro | 0:45 |
| 12 | Recomendaciones para PythonAnywhere | Alejandro | 0:40 |
| 13 | Limitación del plan gratuito | Alejandro | 0:30 |
| 14 | Ética y concientización | Alejandro | 0:50 |
| 15 | Conclusión | Alejandro y Xavier | 0:25 |
| 16 | Anexo: fuentes | (no se expone) | - |

**Total estimado: 8:55.** Las líneas «Fuente (no leer)» de las notas no se dicen en voz alta: están ahí porque la pauta pide las fuentes en las notas.

## 3. Lámina por lámina: qué decir y qué hacer


### Lámina 1: Portada

**Hacer:**
- Presentación abierta en modo presentador.
- Xavier habla; Alejandro está al lado del notebook, con la terminal lista para la demostración.

**Xavier dice** (unos 15 s):

> Buenos días. Somos Xavier Romero y Alejandro Figueroa. Les vamos a mostrar cómo revisamos la seguridad de nuestra aplicación de listas de compras, que está publicada en internet. Yo voy a presentar el análisis del código y las pruebas, y Alejandro, las dependencias, la publicación y la parte ética.


### Lámina 2: Qué revisamos y cómo lo hicimos

**Hacer:**
- Señalar la tarjeta «Operación elegida».
- Al mencionar los roles, señalar las dos tarjetas de abajo.

**Xavier dice** (unos 25 s):

> Nuestra aplicación permite crear listas de compras y agregarles productos con su cantidad y su precio. Cada persona solo puede ver sus propias listas. Para esta revisión elegimos una sola acción: agregar o editar un producto. Ahí revisamos dos datos que se comportan distinto: la cantidad, que es obligatoria y tiene un límite, y el precio, que es opcional. Todo lo probamos en una copia de la aplicación en nuestro computador, con datos inventados.


### Lámina 3: SonarQube: lo que midió y lo que no

**Hacer:**
- Señalar en la captura el «Passed» del Quality Gate y las tres «A».
- Señalar la fila de abajo (inicial → final).
- Terminar en el recuadro amarillo de límites.

**Xavier dice** (unos 45 s):

> Para revisar el código usamos SonarQube, una herramienta que lee el código y avisa de posibles problemas. Hicimos una revisión el 15 de octubre, sobre la versión publicada, y otra el 20, ya con las correcciones. Solo dejamos fuera carpetas que no son nuestras, como librerías externas y archivos que se generan solos. El resultado general aprobó y no encontró vulnerabilidades. Pero eso no significa que la aplicación sea segura: la herramienta no vio que la clave secreta era débil ni que se podía guardar una cantidad cero. Eso lo encontramos revisando a mano. Y el cero por ciento de cobertura del inicio no significa que no hubiera pruebas: simplemente no habíamos cargado ese informe.


### Lámina 4: Observación 1

**Hacer:**
- Señalar en la captura el aviso verde «Closed (Fixed)».
- Señalar «Antes» y «Después» sin leer el código.
- Terminar en la tarjeta verde «Decisión».

**Xavier dice** (unos 35 s):

> La primera observación está en la parte que muestra el subtotal en pesos, con sus puntos de miles. Para eso se usaba un patrón de búsqueda de texto que, con textos muy largos, puede volverse muy lento, y por eso SonarQube lo marca. Pero miramos el contexto: aquí solo recibe números cortos y funciona en el computador del propio usuario, así que nadie puede usarlo para atacar la aplicación. Es un tema de calidad, no de seguridad. Como arreglarlo era fácil, lo cambiamos por el formato de números que ya trae el navegador para Chile, y comprobamos que muestra exactamente lo mismo.


### Lámina 5: Observación 2

**Hacer:**
- Señalar en la captura el aviso verde «Closed (Fixed)».
- Señalar la fila «otro-usuario.pythonanywhere.com» de la tabla: pasa de Sí a No.

**Xavier dice** (unos 40 s):

> La segunda observación parecía menor: SonarQube avisó que un mismo texto estaba repetido tres veces en la configuración. Al revisarlo vimos algo más importante: la aplicación aceptaba cualquier dirección terminada en pythonanywhere.com, no solo la nuestra. O sea, confiaba en sitios de otros usuarios de la misma plataforma. Lo comprobamos con la configuración real: antes aceptaba el dominio de otro usuario y ahora no. Además, ese permiso tan amplio escondía dos errores: nuestro propio dominio no estaba declarado y había un error de tipeo. La alerta vino de la herramienta, pero la conclusión de seguridad fue nuestra.


### Lámina 6: OWASP Top 10:2025

**Hacer:**
- Señalar cada tarjeta mientras se nombra.
- Terminar señalando la nota de abajo sobre inyección.

**Xavier dice** (unos 30 s):

> Relacionamos lo encontrado con dos categorías del OWASP Top 10, que es la lista de los riesgos más comunes en aplicaciones web. La primera es configuración insegura: el permiso amplio que acabamos de ver y la clave secreta débil, que además estaba copiada en un archivo de ejemplo del proyecto. La segunda es diseño inseguro: nunca se definió un límite para la cantidad, así que no existía ningún control. No usamos la categoría de inyección porque no tenemos ninguna evidencia que la respalde.


### Lámina 7: Reglas de los dos datos

**Hacer:**
- Señalar la columna de cantidad y luego la de precio.
- Recorrer las tres tarjetas de abajo de izquierda a derecha.

**Xavier dice** (unos 30 s):

> Aquí están las reglas de los dos datos. La cantidad es obligatoria: un número entero entre 1 y 999. El precio es opcional; si queda vacío o en cero, la aplicación lo marca como «sin precio». Abajo se ve lo más importante: el límite que pone la página web solo ayuda al usuario, y cualquiera se lo puede saltar. La revisión de verdad ocurre en el servidor, antes de guardar. Si el dato no cumple, no se guarda y se muestra el error.


### Lámina 8: La mejora: antes y después

**Hacer:**
- Señalar el recuadro rojo «Antes» y luego el verde «Después».

**Xavier dice** (unos 25 s):

> Esta es la mejora. Antes, el campo aceptaba cero y no tenía máximo. Ahora tiene dos reglas: mínimo uno y máximo 999. La pusimos en la base de la aplicación, para que se cumpla en cualquier lugar donde se cree o edite un producto. No cambia la base de datos, y revisamos que ningún producto ya guardado quedara fuera de rango.


### Lámina 9: Casos ejecutados y demostración

**Hacer:**
- Señalar las filas rojas de la columna «Antes».
- Al decir «se los muestro», cambiar a la terminal (Alt+Tab) y ejecutar el comando de la demostración.
- Volver a la presentación cuando aparezca «OK».

**Xavier dice** (unos 60 s):

> Para probarlo usamos pruebas automáticas que mandan los datos directo al servidor, sin pasar por la página. Probamos valores normales, valores fuera de rango y los límites exactos, uno y 999. Lo importante es el orden: primero escribimos las pruebas y las corrimos con el código original. Fallaron cuatro de trece, porque la aplicación guardó un producto con cantidad cero. Ese es nuestro «antes». Después de la mejora pasan todas. Se los muestro en vivo. [Mientras corre:] Esta prueba intenta guardar un producto con cantidad cero directo en el servidor… y como ven, termina en «ok»: la aplicación lo rechazó.

**Comando de la demostración** (ya escrito en la terminal):

```bash
python manage.py test shopping.tests.ShoppingItemValidationTests.test_backend_crear_con_cantidad_cero_no_guarda -v 2
```
Primero aparecen varias líneas «Applying...» (es normal). Al final debe decir `... ok` y `OK`.


### Lámina 10: Trazabilidad e ISO/IEC 27034

**Hacer:**
- Recorrer la fila de íconos de izquierda a derecha.
- Señalar las cuatro tarjetas de abajo sin leer las siglas.

**Xavier dice** (unos 40 s):

> Así se ve el proceso completo. Primero definimos la regla, después escribimos la prueba, luego aplicamos la corrección, la verificamos en tres lugares —nuestro computador, una copia con las mismas versiones del servidor y la aplicación publicada— y guardamos la evidencia, todo con fecha. Esto lo relacionamos con la norma ISO 27034, que propone justamente eso: que cada control de seguridad tenga una regla clara y una forma de demostrar que funciona. Seguimos su enfoque, pero no decimos que el proyecto esté certificado. Ahora le paso la palabra a Alejandro.


### Lámina 11: Python y dependencias

**Hacer:**
- Señalar la fila de Django.
- Terminar en el recuadro naranjo de abajo.

**Alejandro dice** (unos 45 s):

> Yo revisé las piezas externas que usa la aplicación. El servidor usa Python 3.12, que tiene soporte de seguridad hasta 2028. En Django, que es la base de la aplicación, encontramos dos cosas: nuestro computador y el servidor tenían versiones distintas, y el servidor estaba una versión atrás de una actualización que corrige cuatro fallas de seguridad. Antes de actualizar comprobamos que era un cambio menor y que todas las pruebas seguían pasando; recién ahí actualizamos. De las otras dos librerías, una estaba al día y la otra no coincidía con la lista oficial, así que la fijamos. La causa de fondo era que la lista aceptaba cualquier versión nueva; ahora todas quedaron fijas.


### Lámina 12: Recomendaciones para PythonAnywhere

**Hacer:**
- Señalar las tres fichas de arriba (una verde, dos rojas).
- Luego la tarjeta 1 y la tarjeta 2.

**Alejandro dice** (unos 40 s):

> Revisamos la configuración del servidor. El modo de depuración estaba bien desactivado. Lo primero que recomendamos fue cambiar la clave secreta: estaba marcada como débil y además estaba guardada en el repositorio. Generamos una nueva que solo existe en el servidor; el único costo es que los usuarios deben volver a iniciar sesión. Lo segundo fue declarar exactamente nuestro dominio, porque la aplicación funcionaba solo gracias al permiso amplio que eliminamos. El orden era clave: si publicábamos el código antes de corregir esto, el sitio se caía. Las dos recomendaciones ya están aplicadas y verificadas.


### Lámina 13: Limitación del plan gratuito

**Hacer:**
- Señalar el «1 mes» grande.
- Terminar en la tarjeta verde «Mitigación aplicada».

**Alejandro dice** (unos 30 s):

> Nuestro plan de PythonAnywhere es gratuito y tiene una limitación concreta: la aplicación se apaga al mes si nadie entra a renovarla. Si eso pasa, el sitio deja de estar disponible aunque el código esté perfecto. La nuestra vencía el 24 de octubre, en dos días más; ya la renovamos hasta el 21 de noviembre. Además, por la fecha en que creamos la cuenta, no tenemos MySQL y usamos SQLite. Es una limitación del plan, no un problema de seguridad.


### Lámina 14: Ética y concientización

**Hacer:**
- Señalar la tarjeta verde, luego la roja y luego «Nuestra decisión».
- Terminar en la franja oscura de concientización.

**Alejandro dice** (unos 50 s):

> En la parte ética, dos cosas que sí hicimos: mostrar los hallazgos reales, incluidos nuestros propios errores, sin esconder código de la herramienta para mejorar el resultado; y tratar la clave secreta como secreta: confirmamos que estaba expuesta sin mostrarla nunca. Y dos cosas que no haríamos: inventar o maquillar resultados para aprobar, y hacer pruebas en sitios de otras personas o con datos reales. Por eso probamos en una copia con datos inventados, y en el sitio publicado solo verificamos nuestra propia aplicación, con un usuario de prueba que después borramos. Como acción de concientización proponemos un checklist de cinco minutos antes de subir código: que no vayan claves, revisar la configuración, que las pruebas pasen y que el archivo de secretos no se suba. Ya está publicado en el proyecto y queremos presentarlo al curso.


### Lámina 15: Conclusión

**Hacer:**
- Alejandro dice su parte y le devuelve la palabra a Xavier, que cierra.
- Dejar esta lámina fija durante las preguntas.

**Alejandro dice** (unos 10 s):

> Para cerrar: SonarQube nos ayudó a orientarnos, pero los problemas más serios los encontramos revisando a mano.

**Xavier dice** (unos 15 s):

> Y un control de seguridad solo vale si se puede demostrar: regla, prueba, corrección y evidencia. Todo lo que recomendamos ya está aplicado. Muchas gracias; quedamos atentos a sus preguntas.

## 4. Preguntas probables (respuestas en palabras simples)

### Para Xavier

**¿Por qué pusieron la regla en el modelo y no solo en el formulario?**
Porque el modelo es la base que usan todas las partes de la aplicación. Así la regla se cumple al crear, al editar y desde el panel de administración, sin repetirla en cada lugar.

**¿Por qué 999 como máximo?**
Es una regla de negocio que definimos: en una lista de compras de una casa nadie necesita mil unidades de un producto, y un número absurdo descuadra el presupuesto. Si hubiera que cambiarla, es un solo número, y las pruebas de los límites lo verifican.

**¿Qué pasa con los productos que ya estaban guardados?**
La regla no modifica nada de lo que ya existe; se aplica cuando alguien crea o edita un producto. Igual revisamos producción: ninguno de los 15 productos guardados estaba fuera de rango.

**¿Por qué el precio no cambió?**
Porque su regla ya funcionaba bien: rechaza negativos y texto, y trata el vacío como «sin precio». La pauta pide no tocar un control correcto, así que lo confirmamos con pruebas nuevas.

**¿Que el Quality Gate apruebe significa que la app es segura?**
No. Es una revisión automática con límites. No vio la clave débil ni la falta de un límite en la cantidad; eso lo encontramos revisando a mano.

**¿Por qué SonarQube marca un 64,7 % de cobertura y otra herramienta dice más?**
Cada herramienta mide distinto: SonarQube cuenta líneas y también caminos dentro del código. Ninguna de las dos cifras prueba por sí sola que la aplicación sea segura.

**¿Por qué el permiso amplio era un problema si la app igual pide inicio de sesión?**
Porque la aplicación confiaba en sitios que no controlamos, los de otros usuarios de la plataforma. Eso debilita protecciones que dependen de saber desde dónde llega una petición. Además, escondía errores reales de nuestra configuración.

**¿Por qué no corrigieron las 6 alertas que quedan?**
Son de orden y legibilidad del código, como textos repetidos o una función larga, y no afectan la seguridad. Las dejamos como mejora pendiente con fundamento, que es una de las decisiones que permite la pauta.

**¿Qué es un ASC en la norma ISO 27034?**
Un control de seguridad junto con la forma de comprobar que funciona. En nuestro caso, el control es la regla de la cantidad y la comprobación son las pruebas.

**¿Qué diferencia hay entre configuración insegura (A02) y diseño inseguro (A06)?**
En A02 el código puede estar bien, pero se configuró mal al publicarlo. En A06 el problema es anterior: nunca se definió la regla, y por eso no había control.

**¿De dónde sacaron los conceptos de ISO 27034?**
La norma es de pago. Usamos la página oficial de ISO y las vistas previas oficiales del documento.

### Para Alejandro

**¿Por qué actualizaron Django si la pauta no lo exige?**
Porque la versión nueva corregía cuatro fallas de seguridad y era un cambio menor, de la misma familia de versiones. Antes de actualizar revisamos las notas de la versión y que todas las pruebas pasaran.

**¿Por qué su computador y el servidor tenían versiones distintas?**
Porque la lista de dependencias decía «cualquier versión desde la 5.0», y cada entorno instaló una distinta. Ahora la lista fija versiones exactas en los dos.

**Si el repositorio es privado, ¿la clave igual era un riesgo?**
Sí. Cualquiera con acceso al repositorio, a una copia o a un respaldo podía verla, y además era débil. Una clave que estuvo guardada en el repositorio se considera expuesta y se cambia.

**¿Qué pasa al cambiar la clave secreta?**
Los usuarios tienen que volver a iniciar sesión y dejan de funcionar los enlaces pendientes, como los de recuperar contraseña. Para esta aplicación es aceptable.

**¿La limitación de PythonAnywhere es una falla de seguridad?**
No. Es una regla del plan gratuito: la aplicación se apaga si no se renueva cada mes. Afecta la disponibilidad, no la seguridad.

**¿Probaron en producción? La pauta dice que se use una copia local.**
Las pruebas de validación se hicieron en la copia local. En producción solo verificamos que nuestra propia aplicación funcionara después de publicarla, con un usuario de prueba que borramos al terminar. Nunca tocamos datos reales ni sitios de otros.

**¿Qué harían si encuentran una falla en la aplicación de otra persona?**
No aprovecharla: avisar a la persona o a la plataforma de forma responsable, sin entrar a sus datos.

**¿Cómo saben que la acción de concientización sirve?**
Es concreta y se puede medir: el checklist ya está publicado en el proyecto, y en los siguientes envíos de código se puede revisar si se coló alguna clave o si falla la revisión de configuración.

## Mantenimiento (notas internas, no se entregan)

- **Renovar la app cada mes:** pestaña **Web** → **Run until 1 month from today**. PythonAnywhere envía un correo de aviso una semana antes.
- **SonarQube:** se inicia con `~/tools/start-sonarqube.sh` y se usa en http://localhost:9000.
  - Para escanear: `SONAR_TOKEN=<token> sonar-scanner` desde la raíz del proyecto.
  - El token usado durante la revisión ("claude code") se revocó el 20-10. Sigue vigente tu token "desarrollo-seguro-django" del 15-10; si no lo tienes guardado, crea uno nuevo en *My Account → Security*.
- **PythonAnywhere:** el token de API usado para el despliegue se revocó el 20-10. La cuenta quedó con un token nuevo que nadie ha usado; puedes ignorarlo.
- **Reconstruir la presentación:** el generador está en `fuente_presentacion/build.js` (requiere `pptxgenjs`).
