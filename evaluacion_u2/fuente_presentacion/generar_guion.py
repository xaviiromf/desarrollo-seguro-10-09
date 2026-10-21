"""Genera GUION_Y_PREGUNTAS.md a partir de guion.json (la misma fuente de las notas del PPTX)."""
import json
import pathlib
import re

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI.parent / "GUION_Y_PREGUNTAS.md"
GUION = json.loads((AQUI / "guion.json").read_text())

PREPARACION = """## 1. Antes de empezar: qué tener preparado

**Resumen:** la presentación se proyecta con **LibreOffice Impress** (tu notebook usa Linux y ahí no existe PowerPoint). La **demostración en vivo ocurre en la lámina 9** y consiste en ejecutar una prueba automática en el **proyecto local**, con la versión ya corregida. No hace falta levantar el servidor ni usar PythonAnywhere.

### Días antes
- [ ] Hacer al menos **dos ensayos juntos, con cronómetro**. La meta es terminar entre 8:30 y 9:30.
- [ ] Alejandro abre los enlaces de las fuentes de sus láminas (11 a 13) para conocerlos: la pauta pide no limitarse a copiar a una IA.
- [ ] Los dos leen las preguntas probables (sección 4) y hacen un simulacro: uno pregunta y el otro responde.
- [ ] Entregar el ZIP en la plataforma del curso.

### La noche anterior, paso A: dejar listo el entorno local (10 min, Xavier)
Abre una terminal (**Super + Enter**) y ejecuta, uno por uno:
```bash
cd ~/Projects/desarrollo-seguro/10-09/django-project
git branch --show-current        # main o evaluacion-u2: las dos tienen el mismo código
source venv/bin/activate         # el prompt debe mostrar (venv)
python -m django --version       # debe decir 6.1.2
python manage.py check           # debe decir: System check identified no issues
python manage.py test shopping   # debe terminar en: Ran 25 tests ... OK
```
- El proyecto necesita el archivo `.env` local, que ya existe. No lo abras ni lo muestres.
- Si algo falla, ejecuta `pip install -r requirements.txt` con el venv activo y repite.
- Las pruebas usan una base de datos temporal que se crea y se borra sola: no tocan datos reales.

### La noche anterior, paso B: ensayo técnico con una pantalla externa (15 min, Xavier)
Si tienes un TV o monitor, conéctalo y ensaya exactamente lo que harás en la sala. Al conectarlo, Omarchy lo trata como una **segunda pantalla**.

Comandos de la terminal de la demostración (los usarás en el paso 3):
```bash
cd ~/Projects/desarrollo-seguro/10-09/django-project && source venv/bin/activate && clear
python manage.py test shopping.tests.ShoppingItemValidationTests.test_backend_crear_con_cantidad_cero_no_guarda -v 2
```

1. Pasa el foco a la pantalla externa con **Ctrl + Alt + Tab**.
2. Con el foco en la pantalla externa, pulsa **Super + 5**. Abre ahí el PPTX con LibreOffice Impress y pulsa **F5** para iniciar la presentación.
3. Sin cambiar de pantalla, pulsa **Super + 6** y abre una terminal (**Super + Enter**). Ejecuta la primera línea de los comandos de arriba y escribe la segunda **sin pulsar Enter**. Agranda la letra (**Ctrl + Shift + +**) para que se lea desde el fondo de la sala.
4. Vuelve a la presentación con **Super + 5**.
5. En la pantalla del notebook, deja abierto el PDF del guion para seguir lo que dices: con este método no se usa la consola del presentador.

Si al conectar el TV algo no funciona como se describe, anota qué pasó. En la sala tendrás 15 minutos para resolverlo, y siempre está el plan B.

### El día de la presentación (30 minutos antes)
- [ ] Cargador conectado y adaptador HDMI o USB-C a mano.
- [ ] Notificaciones silenciadas y programas innecesarios cerrados.
- [ ] Repetir los pasos 1 a 4 del ensayo técnico con el proyector de la sala.
- [ ] Probar una vez el comando de la demostración (Enter y comprobar que termina en `OK`). Después escribir `clear` y recuperar el comando con la flecha hacia arriba, **sin pulsar Enter**.
- [ ] Volver a la presentación (**Super + 5**) en la lámina 1.
- [ ] **Plan B:** en **Super + 7**, también en la pantalla externa, dejar abierta la imagen `evaluacion_u2/evidencia/capturas/02_despues_validacion.png`.
- [ ] Una pestaña del navegador con https://actividaddjango1.pythonanywhere.com, por si piden ver la app (solo navegar).
- [ ] **Respaldo:** el PPTX y el ZIP también en un pendrive.

### La demostración en vivo, paso a paso (lámina 9, unos 20 segundos)
1. Di el texto de la lámina 9 hasta «Se los muestro en vivo».
2. Pulsa **Super + 6**: aparece la terminal con el comando ya escrito.
3. Pulsa **Enter**. Primero pasan varias líneas «Applying…»; es normal.
4. Mientras corre, di: «Esta prueba intenta guardar un producto con cantidad cero directo en el servidor…».
5. Cuando aparezcan `... ok` y `OK`, señálalos: «…y como ven, termina en ok: la aplicación lo rechazó».
6. Pulsa **Super + 5** para volver a la presentación y avanza con la flecha derecha a la lámina 10.

**Si algo falla** (la terminal no aparece o la prueba da error): no improvises. Pulsa **Super + 7**, muestra la captura del plan B y di: «Esta es la misma prueba ejecutada el 19 de octubre; termina en OK». Luego vuelve con **Super + 5**.

### Qué NO mostrar nunca en pantalla
- El archivo `.env`, ni local ni de PythonAnywhere, ni ninguna clave secreta.
- La consola de PythonAnywhere, porque su historial puede tener datos sensibles.

### Roles durante la presentación
- **Xavier:** controla el notebook, expone las láminas 1 a 10 y hace la demostración.
- **Alejandro:** expone las láminas 11 a 14 y comparte la 15. Le pide a Xavier «siguiente» para avanzar.
- **En las preguntas:** responde quien expuso ese tema. Si no saben algo, decirlo con honestidad: «No lo verificamos; lo podemos revisar».
"""

PREGUNTAS = """## 4. Preguntas probables (respuestas en palabras simples)

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
"""


def mmss(seg):
    return f"{seg // 60}:{seg % 60:02d}"


def main():
    previo = SALIDA.read_text() if SALIDA.exists() else ""
    mantenimiento = previo[previo.index("## Mantenimiento"):] if "## Mantenimiento" in previo else ""

    total = 0
    filas, laminas = [], []
    for n, g in enumerate(GUION, 1):
        if not g["partes"]:
            filas.append(f"| {n} | {g['titulo']} | (no se expone) | - |")
            continue
        seg = sum(p["seg"] for p in g["partes"])
        total += seg
        quien = " y ".join(dict.fromkeys(p["quien"].capitalize() for p in g["partes"]))
        filas.append(f"| {n} | {g['titulo']} | {quien} | {mmss(seg)} |")

        bloque = [f"### Lámina {n}: {g['titulo']}", "", "**Hacer:**"]
        bloque += [f"- {h}" for h in g["hacer"]]
        for p in g["partes"]:
            bloque += ["", f"**{p['quien'].capitalize()} dice** (unos {p['seg']} s):", ""]
            bloque += [f"> {linea}" for linea in p["decir"].split("\n")]
        if g.get("demo"):
            bloque += ["", "**Comando de la demostración** (ya escrito en la terminal):", "", "```bash", g["demo"], "```",
                       "Primero aparecen varias líneas «Applying...» (es normal). Al final debe decir `... ok` y `OK`."]
        laminas.append("\n".join(bloque))

    palabras = sum(len(re.sub(r"\[.*?\]", "", p["decir"]).split()) for g in GUION for p in g["partes"])
    tabla = "\n".join(["| Lámina | Tema | Expone | Tiempo |", "|---|---|---|---|", *filas])
    texto = f"""# Guion de la presentación y preparación

Lo que dice cada uno está también en las **notas del orador** del PPTX. La idea no es leerlo palabra por palabra, sino decirlo con sus propias palabras.

**Regla general:** en las láminas se ven los términos técnicos (nombres de reglas, código, archivos), pero al hablar **no los nombramos**: explicamos la idea en palabras simples. Si el profesor pregunta por un término, ahí sí lo explicamos.

{PREPARACION}
## 2. Reparto y tiempos

El texto hablado suma unas {palabras} palabras: unos {round(palabras / 150, 1)} minutos a ritmo normal, más la demostración y las transiciones.

{tabla}

**Total estimado: {mmss(total)}.** Las líneas «Fuente (no leer)» de las notas no se dicen en voz alta: están ahí porque la pauta pide las fuentes en las notas.

## 3. Lámina por lámina: qué decir y qué hacer

{chr(10).join(chr(10) + l + chr(10) for l in laminas)}
{PREGUNTAS}
{mantenimiento}"""
    SALIDA.write_text(texto.rstrip() + "\n")
    print("OK", SALIDA, "| total", mmss(total), "|", palabras, "palabras")


if __name__ == "__main__":
    main()
