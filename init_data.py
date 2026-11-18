"""
Script de inicialización de datos semilla (solo desarrollo local) con Pesos Chilenos (CLP).
Las contraseñas se leen de INIT_ADMIN_PASSWORD e INIT_DEMO_PASSWORD: nunca se dejan escritas en el código.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket_project.settings')
django.setup()

from django.contrib.auth.models import User
from shopping.models import ShoppingList, ShoppingItem, Priority

def _password(variable):
    valor = os.environ.get(variable)
    if not valor:
        sys.exit(f"Define {variable} antes de ejecutar este script.")
    return valor


def run():
    print("Iniciando creación de superusuario y datos semilla en Pesos Chilenos (CLP)...")

    # 1. Crear o actualizar usuario admin / admin
    admin_user, created = User.objects.get_or_create(username='admin')
    admin_user.set_password(_password('INIT_ADMIN_PASSWORD'))
    admin_user.email = 'admin@pastelmarket.local'
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    if created:
        print("✓ Superusuario 'admin' creado exitosamente.")
    else:
        print("✓ Superusuario 'admin' actualizado.")

    # 2. Crear usuario secundario para demostración de aislamiento
    demo_user, _ = User.objects.get_or_create(username='maria')
    demo_user.set_password(_password('INIT_DEMO_PASSWORD'))
    demo_user.email = 'maria@pastelmarket.local'
    demo_user.save()
    print("✓ Usuario de prueba 'maria' preparado.")

    # 3. Limpiar listas de prueba previas para recargar con CLP y productos sin precio
    ShoppingList.objects.filter(user__in=[admin_user, demo_user]).delete()

    # Lista 1: Alta prioridad (Urgente)
    list_urgent = ShoppingList.objects.create(
        user=admin_user,
        name='Despensa Esencial de la Semana',
        description='Víveres urgentes para cocinar durante la semana.',
        priority=Priority.HIGH
    )
    ShoppingItem.objects.create(
        shopping_list=list_urgent,
        name='Leche Entera 1L',
        brand='Colun',
        quantity=3,
        unit_price=1290,
        is_purchased=True
    )
    ShoppingItem.objects.create(
        shopping_list=list_urgent,
        name='Huevos de Campo (Bandeja 12)',
        brand='La Granja',
        quantity=2,
        unit_price=3990,
        is_purchased=False
    )
    ShoppingItem.objects.create(
        shopping_list=list_urgent,
        name='Pan Molde Artesanal',
        brand='Ideal',
        quantity=1,
        unit_price=2490,
        is_purchased=False
    )
    ShoppingItem.objects.create(
        shopping_list=list_urgent,
        name='Café Molido Premium',
        brand='Juan Valdez',
        quantity=1,
        unit_price=0,
        has_unknown_price=True,
        is_purchased=False
    )

    # Lista 2: Media prioridad (Verdulería)
    list_medium = ShoppingList.objects.create(
        user=admin_user,
        name='Verdulería & Frutería Fresca',
        description='Frutas de temporada para batidos y ensaladas.',
        priority=Priority.MEDIUM
    )
    ShoppingItem.objects.create(
        shopping_list=list_medium,
        name='Manzanas Fuji (Bolsa 1kg)',
        brand='Huerto San Pedro',
        quantity=2,
        unit_price=1890,
        is_purchased=False
    )
    ShoppingItem.objects.create(
        shopping_list=list_medium,
        name='Paltas Hass (Malla 1kg)',
        brand='Nacional',
        quantity=1,
        unit_price=4500,
        is_purchased=False
    )
    ShoppingItem.objects.create(
        shopping_list=list_medium,
        name='Plátanos (Racimo 1kg)',
        brand='Ecuador Fresh',
        quantity=1,
        unit_price=1390,
        is_purchased=True
    )
    ShoppingItem.objects.create(
        shopping_list=list_medium,
        name='Frutillas Orgánicas Frescas',
        brand='Feria Local',
        quantity=2,
        unit_price=0,
        has_unknown_price=True,
        is_purchased=False
    )

    # Lista 3: Baja prioridad (Antojos)
    list_low = ShoppingList.objects.create(
        user=admin_user,
        name='Antojos & Noche de Películas',
        description='Snacks y dulces para el fin de semana.',
        priority=Priority.LOW
    )
    ShoppingItem.objects.create(
        shopping_list=list_low,
        name='Chocolate Amargo 70%',
        brand='Lindt',
        quantity=2,
        unit_price=3890,
        is_purchased=False
    )
    ShoppingItem.objects.create(
        shopping_list=list_low,
        name='Palomitas de Maíz Microondas',
        brand='Act II',
        quantity=3,
        unit_price=1190,
        is_purchased=False
    )

    # Lista de prueba para 'maria'
    list_maria = ShoppingList.objects.create(
        user=demo_user,
        name='Lista Personal de María',
        description='Compras de limpieza para el hogar.',
        priority=Priority.HIGH
    )
    ShoppingItem.objects.create(
        shopping_list=list_maria,
        name='Detergente Líquido 3L',
        brand='Ariel',
        quantity=1,
        unit_price=9890,
        is_purchased=False
    )

    print("✓ Datos semilla actualizados exitosamente en Pesos Chilenos (CLP) con productos con y sin precio.")

if __name__ == '__main__':
    run()
