import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from shopping.models import ShoppingItem, ShoppingList


class Command(BaseCommand):
    help = "Crea dos cuentas ficticias del laboratorio con una lista de ejemplo. Las contraseñas vienen del entorno."

    def handle(self, *args, **options):
        cuentas = {'qa_ana': 'LAB_PASSWORD_ANA', 'qa_beto': 'LAB_PASSWORD_BETO'}
        for username, variable in cuentas.items():
            password = os.environ.get(variable)
            if not password:
                raise CommandError(f"Falta la variable {variable} en el entorno (ver .env.lab.example).")
            user, _ = User.objects.get_or_create(username=username, defaults={'email': f'{username}@ejemplo.test'})
            user.set_password(password)
            user.save()
            lista, creada = ShoppingList.objects.get_or_create(user=user, name=f'Lista de prueba de {username}')
            if creada:
                ShoppingItem.objects.create(shopping_list=lista, name='Producto ficticio', quantity=2, unit_price=1500)
            self.stdout.write(self.style.SUCCESS(f"Cuenta {username} lista."))
