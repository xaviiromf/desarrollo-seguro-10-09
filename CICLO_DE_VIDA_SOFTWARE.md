# Ciclo Completo de Vida del Software (SDLC)
## Sistema de Listas de Supermercado PastelMarket

Este documento describe de manera exhaustiva el ciclo de vida completo del software (SDLC, *Software Development Life Cycle*) para la aplicación **PastelMarket**, construida con el framework **Django** utilizando vistas basadas en clases (**Class-Based Views**), base de datos **SQLite**, autenticación de usuarios, cálculo reactivo de compras de supermercado, moneda en **Pesos Chilenos (CLP)**, gestión de productos **sin precio**, categorías de productos, límites presupuestarios, exportación y una interfaz moderna estilizada con **Tailwind CSS v3** y **Crispy Forms**.

---

## 1. Fase de Planificación y Análisis de Requerimientos

### 1.1. Propósito y Alcance
El objetivo es proporcionar a los usuarios una herramienta web personal, ágil y visualmente agradable para planificar y ejecutar sus compras de supermercado. La plataforma resuelve el problema de la falta de control presupuestario y desorganización al hacer compras, permitiendo presupuestar producto a producto antes o durante la visita a la tienda, adaptarse a precios desconocidos y compartir la lista fácilmente.

### 1.2. Requerimientos Funcionales (RF)
- **RF-01 (Autenticación y Sesiones):** Registro, inicio y cierre de sesión de usuarios con almacenamiento seguro en base de datos SQLite con contraseñas cifradas (PBKDF2/SHA256).
- **RF-02 (Aislamiento Multi-usuario):** Cada usuario solo puede ver, crear, modificar y eliminar sus propias listas de compras y productos asociados.
- **RF-03 (Múltiples Listas de Compras):** Un usuario puede crear tantas listas como necesite (ej. "Despensa Semanal", "Verdulería", "Asado Familiar").
- **RF-04 (Priorización de Listas):** Cada lista cuenta con un nivel de prioridad (Alta 🔴, Media 🟡, Baja 🟢) y la vista principal permite ordenar y filtrar según esta prioridad.
- **RF-05 (Separación de Vistas):** 
  - *Vista de Listas (Dashboard):* Vista general con métricas, tarjetas de listas, totales estimados, barras de progreso y buscador.
  - *Vista de Detalle:* Vista con la tabla de productos, agregador lateral con Crispy Forms, filtros de estado, selector de categorías y métricas de avance.
- **RF-06 (Gestión de Productos con Categorías):** Cada ítem registra: Nombre del producto, Categoría (Abarrotes, Carnes, Frutas/Verduras, Lácteos, Panadería, Bebidas, Limpieza, Cuidado Personal, Congelados, Snacks, Mascotas, Otros), Marca (opcional), Cantidad y Precio unitario en Pesos Chilenos ($).
- **RF-07 (Opción "Sin Precio" para Productos):** Posibilidad de marcar un producto con precio desconocido (`has_unknown_price = True`). El sistema lo identifica como *"Sin precio / Por definir"*, no sumará un costo fantasma al total acumulado y mostrará advertencias claras al usuario.
- **RF-08 (Cálculo de Totales en Pesos Chilenos - CLP):**
  - Manejo de enteros sin decimales/centavos propio de la moneda nacional chilena.
  - Subtotal por producto = `Cantidad * Precio por unidad` (o 0 si no tiene precio).
  - Total de la lista = Suma de los subtotales de productos valorizados.
  - Filtro de plantilla personalizado `|clp` (ej. `$12.990`).
  - Cálculo reactivo en frontend (JavaScript `calculator.js`) al ingresar cantidad o precio, o al marcar/desmarcar "sin precio".
- **RF-09 (Control de Presupuesto Límite):** Posibilidad de fijar un tope presupuestario voluntario (`budget_limit`) en cada lista. Se calcula porcentaje de avance, monto restante o advertencia destacada de sobregiro con montos excedentes.
- **RF-10 (Control de Estado de Compra y Progreso):**
  - Alternancia reactiva (checkboxes) para marcar productos como comprados.
  - Indicador porcentual de progreso y desglose entre "Gastado" y "Pendiente".
  - Acciones masivas: "Marcar todos" y "Desmarcar todos".
  - Acción "Limpiar comprados" para remover de una sola vez los ítems tachados.
- **RF-11 (Duplicación de Listas):** Capacidad de duplicar cualquier lista previa (con todos sus productos reiniciados en estado pendiente) para reutilizar compras habituales.
- **RF-12 (Exportación y Compartición):**
  - **Exportar CSV/Excel:** Descarga de la lista completa con codificación UTF-8 BOM, delimitada por punto y coma para apertura nativa en Microsoft Excel y Calc.
  - **Compartir por WhatsApp:** Generador de texto enriquecido con formato de viñetas, emojis y totales copiado directamente al portapapeles.
  - **Modo Impresión:** Hoja de estilos de impresión `@media print` para generar listas físicas limpias sin elementos de navegación ni formularios.
- **RF-13 (Búsqueda en Tiempo Real):** Filtrado instantáneo en la tabla de productos mediante teclado en el cliente sin recargas.
- **RF-14 (Panel de Administración):** Acceso a `/admin` para gestionar usuarios, contraseñas, listas y productos con cuenta preconfigurada `admin` / `admin`.

### 1.3. Requerimientos No Funcionales (RNF)
- **RNF-01 (Diseño Visual Moderno con Tailwind CSS):** Interfaz estilizada con Tailwind CSS v3 y paleta armónica (esmeralda, índigo, pizarra, ámbar, rosa) con tarjetas suaves, bordes redondeados y microinteracciones.
- **RNF-02 (Rendimiento y Ligereza):** Vistas procesadas en el servidor mediante Class-Based Views de Django, complementadas con scripts livianos en Vanilla JS para reactividad inmediata sin frameworks pesados.
- **RNF-03 (Configuración desacoplada):** Credenciales y claves en `.env` mediante `python-dotenv`.
- **RNF-04 (Integridad Financiera):** Registro de precios en CLP con enteros positivos (`PositiveIntegerField`), asegurando que no existan centavos ni inconsistencias numéricas.

---

## 2. Fase de Diseño y Arquitectura

### 2.1. Arquitectura MVT (Model - View - Template)
La aplicación sigue la arquitectura estándar de Django implementada al 100% con **Class-Based Views**:

```
[ Cliente Web (Navegador) ]
          │
          ▼  (HTTP Request / CSRF Token / AJAX)
[ URLs Dispatcher (supermarket_project / shopping) ]
          │
          ▼
[ Class-Based Views (CBV) ]
  ├── UserLoginView / UserRegisterView / LogoutView
  ├── ShoppingListListView (Filtros, orden por prioridad, buscador, métricas)
  ├── ShoppingListDetailView (Detalle de productos, categorías, buscador en vivo)
  ├── ShoppingListCreateView / ShoppingListUpdateView / ShoppingListDeleteView
  ├── ShoppingListDuplicateView (Clonación de listas)
  ├── ShoppingListBulkToggleView (Marcar / Desmarcar todos)
  ├── ShoppingListExportCSVView (Generación dinámica de hoja CSV/Excel)
  ├── ShoppingListClearPurchasedView (Eliminación masiva de ítems comprados)
  ├── ShoppingItemCreateView / ShoppingItemUpdateView / ShoppingItemDeleteView
  └── ShoppingItemTogglePurchasedView (Alternancia reactiva con fetch)
          │
     ┌────┴────────────────────────┐
     ▼                             ▼
[ Modelos ORM ]             [ Templates Tailwind + Crispy ]
 (ShoppingList, ShoppingItem) (base.html, list.html, detail.html)
     │                             │
     ▼                             ▼
[ SQLite (db.sqlite3) ]     [ Tailwind CSS + calculator.js ]
```

### 2.2. Modelo Relacional de Base de Datos
- **Tabla `auth_user`**: Usuarios nativos de Django (id, username, password_hash, email, is_staff, is_superuser).
- **Tabla `shopping_shoppinglist`**:
  - `id`: AutoField (PK)
  - `user_id`: ForeignKey (`auth_user.id`, ON DELETE CASCADE)
  - `name`: VarChar(150)
  - `description`: TextField
  - `priority`: Integer (1: Alta, 2: Media, 3: Baja)
  - `budget_limit`: PositiveIntegerField (null=True, blank=True)
  - `created_at`: DateTime
  - `updated_at`: DateTime
- **Tabla `shopping_shoppingitem`**:
  - `id`: AutoField (PK)
  - `shopping_list_id`: ForeignKey (`shopping_shoppinglist.id`, ON DELETE CASCADE)
  - `name`: VarChar(200)
  - `brand`: VarChar(150)
  - `category`: VarChar(30) (Opciones: Abarrotes, Carnes, Lácteos, Frutas/Verduras, etc.)
  - `quantity`: PositiveIntegerField (default: 1)
  - `unit_price`: PositiveIntegerField (default: 0) - Precio en CLP
  - `has_unknown_price`: BooleanField (default: False) - Opción sin precio
  - `is_purchased`: BooleanField (default: False)
  - `created_at`: DateTime

---

## 3. Fase de Implementación y Codificación

### 3.1. Estructura del Código Fuente
```
django-project/
├── .env                           # Variables de entorno confidenciales
├── .gitignore                      # Exclusiones de control de versiones
├── requirements.txt                # Dependencias del proyecto fijadas
├── manage.py                       # CLI administrativo de Django
├── init_data.py                    # Script semilla (admin/admin y datos base)
├── CICLO_DE_VIDA_SOFTWARE.md       # Documentación del SDLC
├── supermarket_project/            # Módulo de configuración global
│   ├── __init__.py
│   ├── settings.py                 # Configuración de Django, Tailwind y Crispy
│   ├── urls.py                     # Enrutador principal y URLs de auth
│   ├── wsgi.py
│   └── asgi.py
├── shopping/                       # Aplicación de compras de supermercado
│   ├── __init__.py
│   ├── admin.py                    # Configuración de panel de administración
│   ├── apps.py
│   ├── forms.py                    # Formularios con Crispy Tailwind
│   ├── models.py                   # Modelos ShoppingList y ShoppingItem (CLP + Sin precio)
│   ├── tests.py                    # Suite de 12 pruebas automatizadas
│   ├── urls.py                     # Enrutador de listas e ítems
│   ├── views.py                    # CBVs completas (CRUD, CSV, Duplicar, Bulk, Toggle)
│   └── templatetags/
│       ├── __init__.py
│       └── shopping_tags.py        # Filtro de formato de moneda chilena (|clp)
├── static/
│   └── shopping/
│       └── js/calculator.js        # Cálculo reactivo en vivo y manejo de 'sin precio'
├── theme/                          # Aplicación de estilos Tailwind CSS
│   ├── package.json
│   ├── tailwind.config.js
│   └── static/css/dist/styles.css  # CSS compilado y minificado
└── templates/
    ├── base.html                   # Layout maestro con navbar y estilos de impresión
    ├── registration/
    │   ├── login.html              # Pantalla de inicio de sesión
    │   └── register.html           # Pantalla de registro de usuarios
    └── shopping/
        ├── shoppinglist_list.html          # Vista de listas (Dashboard de métricas)
        ├── shoppinglist_detail.html        # Vista de detalle con tabla, filtros y acciones
        ├── shoppinglist_form.html          # Formulario crear/editar lista
        ├── shoppinglist_confirm_delete.html# Confirmación de borrado de lista
        └── shoppingitem_form.html          # Formulario edición de ítem
```

### 3.2. Puntos Clave de Implementación
1. **Uso Exclusivo de CBVs:** Cada acción del usuario está respaldada por vistas basadas en clases (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `LoginView`, `View`).
2. **Aislamiento por Usuario:** Las consultas ORM se limitan estrictamente a través del método `get_queryset()`:
   ```python
   def get_queryset(self):
       return ShoppingList.objects.filter(user=self.request.user)
   ```
3. **Cálculo Exacto de Pesos Chilenos (CLP):**
   ```python
   @property
   def total_price(self) -> int:
       if self.is_price_unknown:
           return 0
       return self.quantity * self.unit_price
   ```
4. **Calculadora Frontend Reactiva (`calculator.js`):** Escucha eventos de teclado y cambios en el checkbox `has_unknown_price` para desactivar el campo de precio y reflejar instantáneamente el subtotal proyectado.
5. **Generador de CSV con compatibilidad Excel:** Uso de delimitador `;` y BOM UTF-8 `\ufeff` para que las listas exportadas se abran correctamente en cualquier hoja de cálculo.

---

## 4. Fase de Pruebas y Aseguramiento de Calidad (QA)

### 4.1. Estrategia de Pruebas
Se diseñó y mantuvo una suite completa de pruebas unitarias y de integración (`shopping/tests.py`) ejecutadas con el test runner nativo de Django.

### 4.2. Casos de Prueba Implementados
| ID | Caso de Prueba | Descripción / Resultado Esperado | Estado |
|---|---|---|---|
| **TC-01** | Subtotal de producto en CLP | Verifica que `3 * 1.290 = 3.870` CLP exactos | **PASS** |
| **TC-02** | Manejo de ítem "Sin precio" | Verifica que `total_price = 0` y muestre `"Sin precio"` | **PASS** |
| **TC-03** | Total acumulado de la lista en CLP | Suma exacta de ítems valorizados ignorando los sin precio | **PASS** |
| **TC-04** | Aislamiento de datos entre usuarios | Usuario A no puede ver ni acceder al detalle de Usuario B (404) | **PASS** |
| **TC-05** | Ordenamiento por prioridad | Listas con prioridad Alta aparecen antes que Media y Baja | **PASS** |
| **TC-06** | Creación vía POST con CLP y Sin Precio | Valida persistencia en base de datos de ambos tipos de ítems | **PASS** |
| **TC-07** | Alternancia reactiva de ítem comprado | El estado `is_purchased` cambia de `False` a `True` | **PASS** |
| **TC-08** | Límite de presupuesto y sobregiro | Comprueba cálculo porcentual, saldo restante y alerta de exceso | **PASS** |
| **TC-09** | Duplicación completa de lista | Clona lista con productos reiniciados a pendientes (`is_purchased=False`) | **PASS** |
| **TC-10** | Acciones masivas de marcado/desmarcado | Cambia en lote todos los productos a comprados o pendientes | **PASS** |
| **TC-11** | Exportación a archivo CSV | Valida cabeceras HTTP, codificación UTF-8 BOM, datos y seguridad 404 | **PASS** |
| **TC-12** | Limpiar productos comprados | Elimina solo los ítems marcados, preservando los pendientes | **PASS** |

### 4.3. Ejecución de Pruebas
```bash
./venv/bin/python manage.py test
```
*Salida de validación:*
```
Found 12 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
............
----------------------------------------------------------------------
Ran 12 tests in 10.555s

OK
Destroying test database for alias 'default'...
```

---

## 5. Fase de Despliegue y Puesta en Producción

### 5.1. Despliegue en Plataforma Cloud (PythonAnywhere)
Para una guía detallada paso a paso consulte [PYTHONANYWHERE_DEPLOY.md](file:///home/xavi/Projects/desarrollo-seguro/10-09/django-project/PYTHONANYWHERE_DEPLOY.md).

1. **Clonación del repositorio en la consola Bash de PythonAnywhere:**
   ```bash
   git clone https://github.com/xaviromf-boop/desarrollo-seguro-10-09.git
   cd desarrollo-seguro-10-09/django-project
   ```
2. **Creación del entorno virtual e instalación de dependencias:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 emprendevirtual
   pip install -r requirements.txt
   ```
3. **Variables de entorno de codificación UTF-8:**
   ```bash
   export LANG=C.UTF-8
   export LC_ALL=C.UTF-8
   export PYTHONIOENCODING=utf-8
   ```
4. **Configuración del archivo `.env`:**
   ```bash
   cp .env.example .env
   chmod 600 .env
   ```
   Configurar `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS=3600`.
5. **Migraciones y datos semilla:**
   ```bash
   python manage.py migrate
   python init_data.py
   ```
6. **Recolección de archivos estáticos y verificación:**
   ```bash
   python manage.py collectstatic --noinput
   python manage.py check --deploy
   ```
7. **Pestaña Web de PythonAnywhere:**
   - **Source & Working directory:** `/home/<usuario>/desarrollo-seguro-10-09/django-project`
   - **WSGI file:** Usar la configuración documentada en [pythonanywhere_wsgi.py](file:///home/xavi/Projects/desarrollo-seguro/10-09/django-project/pythonanywhere_wsgi.py).
   - **Static files:** Mapear `/static/` a `staticfiles/` y `/media/` a `media/`.
   - **Reload:** Recargar la aplicación web desde la interfaz.

---

## 6. Fase de Operación, Mantenimiento y Evolución

### 6.1. Copias de Seguridad (Backups)
Dado que la base de datos se almacena en el archivo `db.sqlite3`, la estrategia de respaldo es rápida y segura:
- Realizar copias instantáneas programadas (cron job) mediante el comando SQLite online backup:
  ```bash
  sqlite3 db.sqlite3 ".backup 'backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3'"
  ```

### 6.2. Monitoreo y Auditoría
- Uso del panel de administración (`/admin`) para supervisar usuarios registrados y registros de compras.
- Registro de accesos y errores a través de los logs de Django y el servidor de aplicaciones WSGI.

---
*Documento elaborado para PastelMarket - Sistema de Gestión de Compras de Supermercado con Django CBV, Tailwind CSS, Crispy Forms y SQLite.*
