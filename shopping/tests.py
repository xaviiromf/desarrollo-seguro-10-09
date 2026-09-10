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

    def test_item_total_calculation_clp(self):
        """Verifica que el subtotal en CLP sea exactamente cantidad * precio unitario entero."""
        item = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Leche',
            brand='Colun',
            quantity=3,
            unit_price=1290
        )
        # 3 * 1290 = 3870
        self.assertEqual(item.total_price, 3870)
        self.assertEqual(item.formatted_unit_price, "$1.290")
        self.assertEqual(item.formatted_total_price, "$3.870")

    def test_item_without_price_calculation(self):
        """Verifica el comportamiento de productos marcados como 'sin precio'."""
        item = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Café Molido',
            quantity=2,
            unit_price=0,
            has_unknown_price=True
        )
        self.assertTrue(item.is_price_unknown)
        self.assertEqual(item.total_price, 0)
        self.assertEqual(item.formatted_unit_price, "Sin precio")
        self.assertEqual(item.formatted_total_price, "Sin precio")
        self.assertTrue(self.list1.has_items_without_price)
        self.assertEqual(self.list1.items_without_price_count, 1)

    def test_shopping_list_total_amount_calculation_clp(self):
        """Verifica que el total de la lista sume correctamente los subtotales en CLP ignorando los sin precio."""
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Pan',
            quantity=2,
            unit_price=2490 # 4980
        )
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Huevos',
            quantity=1,
            unit_price=3990 # 3990
        )
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Manzanas',
            quantity=4,
            unit_price=1000 # 4000
        )
        # Producto sin precio
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Especias',
            quantity=1,
            unit_price=0,
            has_unknown_price=True
        )
        # Total esperado: 4980 + 3990 + 4000 = 12970
        self.assertEqual(self.list1.total_amount, 12970)
        self.assertEqual(self.list1.formatted_total_amount, "$12.970")
        # Total unidades físicas: 2 + 1 + 4 + 1 = 8
        self.assertEqual(self.list1.total_units, 8)
        self.assertEqual(self.list1.items_count, 4)
        self.assertEqual(self.list1.items_without_price_count, 1)

    def test_user_data_isolation(self):
        """Asegura que las listas de un usuario no sean accesibles ni visibles por otro usuario."""
        client = Client()
        client.login(username='user1', password='password123')

        response = client.get(reverse('shopping:list_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.list1.name)
        self.assertContains(response, self.list2.name)
        self.assertNotContains(response, self.list_user2.name)

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
        self.assertEqual(lists_in_context[0].priority, Priority.HIGH)
        self.assertEqual(lists_in_context[-1].priority, Priority.LOW)

    def test_create_item_via_post_clp(self):
        """Prueba la creación de un nuevo producto con precio en CLP y sin precio mediante POST."""
        client = Client()
        client.login(username='user1', password='password123')

        post_data = {
            'name': 'Yogurt Batido',
            'brand': 'Soprole',
            'quantity': 4,
            'unit_price': '450',
            'has_unknown_price': False,
        }
        url = reverse('shopping:item_create', kwargs={'list_pk': self.list1.pk})
        response = client.post(url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        item = ShoppingItem.objects.get(name='Yogurt Batido', shopping_list=self.list1)
        self.assertEqual(item.quantity, 4)
        self.assertEqual(item.unit_price, 450)
        self.assertEqual(item.total_price, 1800)

        # Crear producto marcando sin precio
        post_data_unknown = {
            'name': 'Pimienta Negra',
            'brand': '',
            'quantity': 1,
            'unit_price': '',
            'has_unknown_price': True,
        }
        response2 = client.post(url, post_data_unknown, follow=True)
        self.assertEqual(response2.status_code, 200)
        item2 = ShoppingItem.objects.get(name='Pimienta Negra', shopping_list=self.list1)
        self.assertTrue(item2.has_unknown_price)
        self.assertEqual(item2.unit_price, 0)
        self.assertEqual(item2.total_price, 0)

    def test_toggle_purchased_item(self):
        """Verifica la alternancia reactiva del estado 'comprado' de un producto."""
        item = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Queso Gauda',
            quantity=1,
            unit_price=3500,
            is_purchased=False
        )
        client = Client()
        client.login(username='user1', password='password123')

        url = reverse('shopping:item_toggle', kwargs={'pk': item.pk})
        response = client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertTrue(item.is_purchased)
