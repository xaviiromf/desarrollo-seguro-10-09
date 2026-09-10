from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import ShoppingList, ShoppingItem, Priority


class ShoppingModelAndCalculationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.list1 = ShoppingList.objects.create(
            user=self.user1,
            name='Lista 1 de User 1',
            priority=Priority.HIGH
        )
        self.list2 = ShoppingList.objects.create(
            user=self.user1,
            name='Lista 2 de User 1',
            priority=Priority.LOW
        )
        self.list_user2 = ShoppingList.objects.create(
            user=self.user2,
            name='Lista de User 2',
            priority=Priority.HIGH
        )

    def test_item_total_calculation(self):
        """Verifica que el subtotal del producto sea exactamente cantidad * precio unitario."""
        item = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Leche',
            brand='Colun',
            quantity=3,
            unit_price=Decimal('1.50')
        )
        # 3 * 1.50 = 4.50
        self.assertEqual(item.total_price, Decimal('4.50'))

    def test_shopping_list_total_amount_calculation(self):
        """Verifica que el total de la lista sume correctamente todos los subtotales de sus productos."""
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Pan',
            quantity=2,
            unit_price=Decimal('2.00') # Subtotal: 4.00
        )
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Huevos',
            quantity=1,
            unit_price=Decimal('3.50') # Subtotal: 3.50
        )
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Manzanas',
            quantity=4,
            unit_price=Decimal('0.75') # Subtotal: 3.00
        )
        # Total esperado: 4.00 + 3.50 + 3.00 = 10.50
        self.assertEqual(self.list1.total_amount, Decimal('10.50'))
        # Total unidades: 2 + 1 + 4 = 7
        self.assertEqual(self.list1.total_units, 7)
        self.assertEqual(self.list1.items_count, 3)

    def test_user_data_isolation(self):
        """Asegura que las listas de un usuario no sean accesibles ni visibles por otro usuario."""
        client = Client()
        client.login(username='user1', password='password123')

        # El usuario 1 accede al dashboard de listas
        response = client.get(reverse('shopping:list_index'))
        self.assertEqual(response.status_code, 200)
        # Debe contener las listas de user1, pero NO las de user2
        self.assertContains(response, self.list1.name)
        self.assertContains(response, self.list2.name)
        self.assertNotContains(response, self.list_user2.name)

        # Intento de acceder al detalle de la lista de user2 -> Debe dar 404
        forbidden_response = client.get(reverse('shopping:list_detail', kwargs={'pk': self.list_user2.pk}))
        self.assertEqual(forbidden_response.status_code, 404)

    def test_priority_ordering(self):
        """Verifica que el ordenamiento por defecto priorice Alta sobre Baja."""
        ShoppingList.objects.create(
            user=self.user1,
            name='Lista Media',
            priority=Priority.MEDIUM
        )
        client = Client()
        client.login(username='user1', password='password123')

        response = client.get(reverse('shopping:list_index') + '?sort=priority')
        self.assertEqual(response.status_code, 200)
        lists_in_context = list(response.context['shopping_lists'])
        # Prioridad 1 (Alta) debe ir antes de Prioridad 2 (Media) y 3 (Baja)
        self.assertEqual(lists_in_context[0].priority, Priority.HIGH)
        self.assertEqual(lists_in_context[-1].priority, Priority.LOW)

    def test_create_item_via_post(self):
        """Prueba la creación de un nuevo producto mediante POST a la vista CBV."""
        client = Client()
        client.login(username='user1', password='password123')

        post_data = {
            'name': 'Yogurt Griego',
            'brand': 'Chobani',
            'quantity': 4,
            'unit_price': '1.25',
        }
        url = reverse('shopping:item_create', kwargs={'list_pk': self.list1.pk})
        response = client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        item = ShoppingItem.objects.get(name='Yogurt Griego', shopping_list=self.list1)
        self.assertEqual(item.quantity, 4)
        self.assertEqual(item.unit_price, Decimal('1.25'))
        self.assertEqual(item.total_price, Decimal('5.00'))

    def test_toggle_purchased_item(self):
        """Verifica la alternancia reactiva del estado 'comprado' de un producto."""
        item = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Queso',
            quantity=1,
            unit_price=Decimal('2.50'),
            is_purchased=False
        )
        client = Client()
        client.login(username='user1', password='password123')

        url = reverse('shopping:item_toggle', kwargs={'pk': item.pk})
        response = client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.is_purchased)
