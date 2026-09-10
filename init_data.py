"""
Script de inicialización para crear el superusuario 'admin' / 'admin' y datos de prueba.
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket_project.settings')
django.setup()

from django.contrib.auth.models import User
from shopping.models import ShoppingList, ShoppingItem, Priority

def run():
    print("Iniciando creación de superusuario y datos semilla...")

    # 1. Crear usuario admin / admin
    admin_user, created = User.objects.get_or_create(username='admin')
    admin_user.set_password('admin')
    admin_user.email = 'admin@pastelmarket.local'
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    if created:
        print("✓ Superusuario 'admin' creado exitosamente.")
    else:
        print("✓ Superusuario 'admin' actualizado con contraseña 'admin'.")

    # 2. Crear usuario secundario para demostración de aislamiento entre usuarios
    demo_user, _ = User.objects.get_or_create(username='maria')
    demo_user.set_password('maria123')
    demo_user.email = 'maria@pastelmarket.local'
    demo_user.save()
    print("✓ Usuario de prueba 'maria' (pass: maria123) preparado.")

    # 3. Listas de prueba para admin si no existen
    if not ShoppingList.objects.filter(user=admin_user).exists():
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
            unit_price=Decimal('1.35'),
            is_purchased=True
        )
        ShoppingItem.objects.create(
            shopping_list=list_urgent,
            name='Huevos de Campo (Bandeja 12)',
            brand='La Granja',
            quantity=2,
            unit_price=Decimal('3.80'),
            is_purchased=False
        )
        ShoppingItem.objects.create(
            shopping_list=list_urgent,
            name='Pan Molde Artesanal',
            brand='Ideal',
            quantity=1,
            unit_price=Decimal('2.50'),
            is_purchased=False
        )

        # Lista 2: Media prioridad (Fin de semana)
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
            unit_price=Decimal('1.90'),
            is_purchased=False
        )
        ShoppingItem.objects.create(
            shopping_list=list_medium,
            name='Paltas Hass',
            brand='Nacional',
            quantity=4,
            unit_price=Decimal('1.50'),
            is_purchased=False
        )
        ShoppingItem.objects.create(
            shopping_list=list_medium,
            name='Plátanos (Racimo)',
            brand='Ecuador Fresh',
            quantity=1,
            unit_price=Decimal('1.80'),
            is_purchased=True
        )

        # Lista 3: Baja prioridad (Antojos / Repostería)
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
            unit_price=Decimal('4.20'),
            is_purchased=False
        )
        ShoppingItem.objects.create(
            shopping_list=list_low,
            name='Palomitas de Maíz Microondas',
            brand='Act II',
            quantity=3,
            unit_price=Decimal('1.10'),
            is_purchased=False
        )

        print("✓ Listas de ejemplo para 'admin' creadas con prioridades Alta, Media y Baja.")

    # Lista de prueba para 'maria' para demostrar aislamiento
    if not ShoppingList.objects.filter(user=demo_user).exists():
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
            unit_price=Decimal('9.50'),
            is_purchased=False
        )
        print("✓ Lista de ejemplo para 'maria' creada (aislamiento validado).")

    print("Inicialización finalizada exitosamente.")

if __name__ == '__main__':
    run()
