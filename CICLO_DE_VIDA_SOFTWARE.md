# Ciclo Completo de Vida del Software (SDLC)
## Sistema de Listas de Supermercado PastelMarket

Este documento describe de manera exhaustiva el ciclo de vida completo del software (SDLC, *Software Development Life Cycle*) para la aplicación **PastelMarket**, construida con el framework **Django** utilizando vistas basadas en clases (**Class-Based Views**), base de datos **SQLite**, autenticación de usuarios, cálculo reactivo de compras de supermercado y una interfaz moderna con paleta de colores pastel.

---

## 1. Fase de Planificación y Análisis de Requerimientos

### 1.1. Propósito y Alcance
El objetivo es proporcionar a los usuarios una herramienta web personal, rápida y visualmente agradable para planificar sus compras de supermercado. La plataforma resuelve el problema de la falta de control presupuestario y desorganización al hacer compras, permitiendo presupuestar producto a producto antes o durante la visita a la tienda.

### 1.2. Requerimientos Funcionales (RF)
- **RF-01 (Autenticación y Sesiones):** Registro, inicio y cierre de sesión de usuarios con almacenamiento seguro en base de datos SQLite con contraseñas cifradas (PBKDF2/SHA256).
- **RF-02 (Aislamiento Multi-usuario):** Cada usuario solo puede ver, crear, modificar y eliminar sus propias listas de compras y productos asociados.
- **RF-03 (Múltiples Listas de Compras):** Un usuario puede crear tantas listas como necesite (ej. "Despensa Semanal", "Verdulería", "Fiesta de Cumpleaños").
- **RF-04 (Priorización de Listas):** Cada lista cuenta con un nivel de prioridad (Alta 🔴, Media 🟡, Baja 🟢) y la vista principal permite ordenar y filtrar según esta prioridad.
- **RF-05 (Separación de Vistas):** 
  - *Vista de Listas (Dashboard):* Vista general con métricas, tarjetas de listas, totales estimados y buscador.
  - *Vista de Detalle:* Vista independiente con la tabla de productos, agregador rápido y cálculo total.
- **RF-06 (Gestión de Productos):** Cada ítem registra: Nombre del producto, Marca (opcional), Cantidad y Precio por unidad ($).
- **RF-07 (Cálculo de Totales):**
  - Subtotal por producto = `Cantidad * Precio por unidad`.
  - Total de la lista = Suma de los subtotales de todos los productos en la lista.
  - Cálculo reactivo en frontend (JavaScript) al escribir valores, y garantizado en backend (Django ORM y `Decimal`).
- **RF-08 (Control de Estado de Compra):** Posibilidad de tachar/marcar productos como comprados en tiempo real.
- **RF-09 (Panel de Administración):** Acceso a `/admin` para gestionar usuarios, contraseñas, listas y productos con cuenta preconfigurada `admin` / `admin`.

### 1.3. Requerimientos No Funcionales (RNF)
- **RNF-01 (Diseño Visual Pastel):** Interfaz acogedora, moderna, con colores pastel suaves (menta, lavanda, durazno, mantequilla, rosa suave), evitando el típico estilo IA SaaS oscuro/neón.
- **RNF-02 (Rendimiento y Ligereza):** Sin sobrecarga de frameworks pesados de frontend; HTML5 semántico, Vanilla CSS y Vanilla JS.
- **RNF-03 (Configuración desacoplada):** Credenciales y claves en `.env` mediante `python-dotenv`.
- **RNF-04 (Precisión Financiera):** Uso de `Decimal` en base de datos para prevenir errores de coma flotante en cálculos monetarios.

---

## 2. Fase de Diseño y Arquitectura

### 2.1. Arquitectura MVT (Model - View - Template)
La aplicación sigue la arquitectura estándar de Django implementada con **Class-Based Views**:

```
[ Cliente Web (Navegador) ]
          │
          ▼  (HTTP Request / CSRF Token)
[ URLs Dispatcher (supermarket_project / shopping) ]
          │
          ▼
[ Class-Based Views (CBV) ]
  ├── UserLoginView / UserRegisterView
  ├── ShoppingListListView (Filtros, orden por prioridad, KPIs)
  ├── ShoppingListDetailView (Detalle de productos, total general)
  ├── ShoppingItemCreateView / ShoppingItemUpdateView / ShoppingItemDeleteView
  └── ShoppingItemTogglePurchasedView (Reactivo vía fetch/AJAX)
          │
     ┌────┴────────────────────────┐
     ▼                             ▼
[ Modelos ORM ]             [ Templates Pastel ]
 (ShoppingList, ShoppingItem) (base.html, list.html, detail.html)
     │                             │
     ▼                             ▼
[ SQLite (db.sqlite3) ]     [ Vanilla CSS + JS Calculator ]
```

### 2.2. Modelo Relacional de Base de Datos
- **Tabla `auth_user`**: Usuarios nativos de Django (id, username, password_hash, email, is_staff, is_superuser).
- **Tabla `shopping_shoppinglist`**:
  - `id`: AutoField (PK)
  - `user_id`: ForeignKey (`auth_user.id`, ON DELETE CASCADE)
  - `name`: VarChar(150)
  - `description`: TextField
  - `priority`: Integer (1: Alta, 2: Media, 3: Baja)
  - `created_at`: DateTime
  - `updated_at`: DateTime
- **Tabla `shopping_shoppingitem`**:
  - `id`: AutoField (PK)
  - `shopping_list_id`: ForeignKey (`shopping_shoppinglist.id`, ON DELETE CASCADE)
  - `name`: VarChar(200)
  - `brand`: VarChar(150)
  - `quantity`: PositiveInteger (default: 1)
  - `unit_price`: Decimal(10, 2)
  - `is_purchased`: Boolean (default: False)
  - `created_at`: DateTime

### 2.3. Sistema de Diseño Pastel (Design Tokens)
Se definieron variables CSS para mantener consistencia y accesibilidad:
- `--pastel-mint`: `#D4EDDA` (Fondo de éxito, prioridad baja)
- `--pastel-honey`: `#FEF3C7` (Prioridad media, avisos)
- `--pastel-rose`: `#FDE8E8` (Prioridad alta, acciones destructivas)
- `--pastel-lavender`: `#EAE6F8` (Acentos de navegación e información)
- `--pastel-peach`: `#FFE5D9` (Insignias de marcas de productos)
- `--bg-app`: `#F7F5F0` (Fondo general cálido, orgánico y suave)
- `--text-main`: `#2C3038` (Texto principal de alto contraste y legibilidad)

---

## 3. Fase de Implementación y Codificación

### 3.1. Estructura del Código Fuente
```
django-project/
├── .env                       # Variables de entorno confidenciales
├── .gitignore                  # Exclusiones de control de versiones
├── requirements.txt            # Dependencias del proyecto fijadas
├── manage.py                   # CLI administrativo de Django
├── init_data.py                # Script semilla (admin/admin y datos de prueba)
├── CICLO_DE_VIDA_SOFTWARE.md   # Documentación del SDLC
├── supermarket_project/        # Módulo de configuración global
│   ├── __init__.py
│   ├── settings.py             # Configuración con dotenv y CBVs
│   ├── urls.py                 # Enrutador principal y URLs de auth
│   ├── wsgi.py
│   └── asgi.py
├── shopping/                   # Aplicación de compras de supermercado
│   ├── __init__.py
│   ├── admin.py                # Configuración de panel de administración
│   ├── apps.py
│   ├── forms.py                # Formularios con mixin pastel
│   ├── models.py               # Modelos ShoppingList y ShoppingItem
│   ├── tests.py                # Suite de pruebas automatizadas
│   ├── urls.py                 # Enrutador de listas e ítems
│   └── views.py                # CBVs completas (List, Detail, CRUD, Auth)
├── static/
│   └── shopping/
│       ├── css/pastel.css      # Hoja de estilos con variables pastel
│       └── js/calculator.js    # Cálculo en tiempo real y AJAX
└── templates/
    ├── base.html               # Layout maestro con navbar pastel
    ├── registration/
    │   ├── login.html          # Pantalla de inicio de sesión
    │   └── register.html       # Pantalla de registro de usuarios
    └── shopping/
        ├── shoppinglist_list.html          # Vista de listas (separada)
        ├── shoppinglist_detail.html        # Vista de detalle (separada)
        ├── shoppinglist_form.html          # Formulario crear/editar lista
        ├── shoppinglist_confirm_delete.html# Confirmación de borrado de lista
        └── shoppingitem_form.html          # Formulario edición de ítem
```

### 3.2. Puntos Clave de Implementación
1. **Uso Exclusivo de CBVs:** Cada acción del usuario está respaldada por una vista genérica (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`, `LoginView`, `LogoutView`).
2. **Aislamiento por Usuario:** Las consultas ORM se limitan estrictamente a través del método `get_queryset()`:
   ```python
   def get_queryset(self):
       return ShoppingList.objects.filter(user=self.request.user)
   ```
3. **Cálculo Exacto de Moneda:** Para evitar pérdidas de precisión inherentes a tipos float, se utiliza `Decimal`:
   ```python
   @property
   def total_price(self) -> Decimal:
       return (Decimal(self.quantity) * self.unit_price).quantize(Decimal('0.01'))
   ```
4. **Calculadora Frontend Reactiva (`calculator.js`):** Escucha eventos `input` en cantidad y precio para actualizar de inmediato el subtotal proyectado sin esperar el envío del formulario.

---

## 4. Fase de Pruebas y Aseguramiento de Calidad (QA)

### 4.1. Estrategia de Pruebas
Se implementó una suite completa de pruebas unitarias y funcionales (`shopping/tests.py`) ejecutadas mediante el test runner de Django.

### 4.2. Casos de Prueba Implementados
| ID | Caso de Prueba | Resultado Esperado | Estado |
|---|---|---|---|
| **TC-01** | Cálculo de subtotal por producto | `3 * 1.50 = 4.50` | **PASS** |
| **TC-02** | Cálculo del total de lista de compras | Suma acumulada exacta de ítems | **PASS** |
| **TC-03** | Conteo total de unidades físicas | Sumatoria de cantidades de todos los ítems | **PASS** |
| **TC-04** | Aislamiento de datos entre usuarios | Usuario A no ve ni puede acceder al detalle de Usuario B (Retorna 404) | **PASS** |
| **TC-05** | Ordenamiento por prioridad | Listas con prioridad Alta aparecen antes que Media y Baja | **PASS** |
| **TC-06** | Alternancia reactiva de ítem comprado | El estado `is_purchased` cambia de `False` a `True` vía POST | **PASS** |

### 4.3. Ejecución de Pruebas
```bash
./venv/bin/python manage.py test
```
*Salida:*
```
Ran 6 tests in 2.036s
OK
```

---

## 5. Fase de Despliegue y Puesta en Producción

### 5.1. Pasos de Instalación en Entorno Local o Servidor
1. **Clonación del repositorio y creación de entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Instalación de dependencias fijadas:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuración del archivo de entorno `.env`:**
   ```env
   DJANGO_SECRET_KEY=tu-clave-secreta-de-produccion
   DJANGO_DEBUG=False
   ALLOWED_HOSTS=tudominio.com,www.tudominio.com,localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```
4. **Aplicación de migraciones:**
   ```bash
   python manage.py migrate
   ```
5. **Ejecución del script semilla (crea admin/admin y datos base):**
   ```bash
   python init_data.py
   ```
6. **Recolección de archivos estáticos (para producción):**
   ```bash
   python manage.py collectstatic --noinput
   ```
7. **Inicio del servidor de producción (vía Gunicorn o Uvicorn):**
   ```bash
   gunicorn supermarket_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
   ```

---

## 6. Fase de Operación, Mantenimiento y Evolución

### 6.1. Copias de Seguridad (Backups)
Dado que la base de datos se almacena en el archivo `db.sqlite3`, la estrategia de respaldo es simple y segura:
- Realizar copias instantáneas programadas (cron job) mediante el comando SQLite online backup:
  ```bash
  sqlite3 db.sqlite3 ".backup 'backups/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3'"
  ```

### 6.2. Monitoreo y Auditoría
- Uso del panel de administración (`/admin`) para supervisar usuarios registrados y registros de actividad.
- Los logs de acceso y errores de Django deben canalizarse a `syslog` o archivos rotativos configurados en `settings.py`.

### 6.3. Roadmap de Evolución Futura
1. **Compartir Listas:** Permitir que múltiples usuarios de un mismo hogar colaboren en tiempo real en una misma lista de compras.
2. **Exportación a PDF / WhatsApp:** Generar resumen de compras optimizado para enviar por mensajería antes de ir al supermercado.
3. **Historial de Precios por Supermercado:** Gráfico comparativo de precios unitarios históricos por marca y producto.
4. **Soporte PWA (Progressive Web App):** Modo sin conexión (*offline-first*) para usar la app dentro de supermercados con baja señal telefónica.

---
*Documento elaborado para PastelMarket - Sistema de Gestión de Compras con Django CBV & SQLite.*
