from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .forms import ShoppingItemForm
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

    def test_budget_limit_and_overbudget_calculations(self):
        """Verifica cálculos de presupuesto máximo y alerta de exceso."""
        self.list1.budget_limit = 10000
        self.list1.save()

        # Agregar ítem dentro del presupuesto
        item1 = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Carne Molida',
            quantity=1,
            unit_price=6000
        )
        self.assertEqual(self.list1.budget_percentage, 60)
        self.assertFalse(self.list1.is_over_budget)
        self.assertEqual(self.list1.remaining_budget, 4000)

        # Agregar ítem que sobrepasa el presupuesto
        item2 = ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Aceite de Oliva',
            quantity=1,
            unit_price=5500
        )
        # Total: 11.500 > 10.000 (115%)
        self.assertEqual(self.list1.total_amount, 11500)
        self.assertEqual(self.list1.budget_percentage, 115)
        self.assertTrue(self.list1.is_over_budget)
        self.assertEqual(self.list1.remaining_budget, -1500)

    def test_duplicate_shopping_list(self):
        """Prueba la duplicación completa de una lista con ítems reiniciados a pendientes."""
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Arroz',
            quantity=2,
            unit_price=1200,
            is_purchased=True
        )
        client = Client()
        client.login(username='user1', password='password123')

        url = reverse('shopping:list_duplicate', kwargs={'pk': self.list1.pk})
        response = client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verificar que se creó la nueva lista
        duplicated = ShoppingList.objects.get(name=f"Copia de {self.list1.name}")
        self.assertEqual(duplicated.user, self.user1)
        self.assertEqual(duplicated.items.count(), self.list1.items.count())
        # Los ítems de la copia deben estar en is_purchased=False
        for it in duplicated.items.all():
            self.assertFalse(it.is_purchased)

    def test_bulk_toggle_items(self):
        """Prueba las acciones masivas de marcar y desmarcar todos los productos."""
        i1 = ShoppingItem.objects.create(shopping_list=self.list1, name='A', quantity=1, unit_price=100, is_purchased=False)
        i2 = ShoppingItem.objects.create(shopping_list=self.list1, name='B', quantity=1, unit_price=200, is_purchased=False)

        client = Client()
        client.login(username='user1', password='password123')

        # Marcar todos
        url = reverse('shopping:list_bulk_toggle', kwargs={'pk': self.list1.pk})
        response = client.post(url, {'action': 'check_all'}, follow=True)
        self.assertEqual(response.status_code, 200)
        i1.refresh_from_db()
        i2.refresh_from_db()
        self.assertTrue(i1.is_purchased)
        self.assertTrue(i2.is_purchased)

        # Desmarcar todos
        response2 = client.post(url, {'action': 'uncheck_all'}, follow=True)
        self.assertEqual(response2.status_code, 200)
        i1.refresh_from_db()
        i2.refresh_from_db()
        self.assertFalse(i1.is_purchased)
        self.assertFalse(i2.is_purchased)

    def test_export_csv(self):
        """Verifica la exportación estructurada a formato CSV y el aislamiento por usuario."""
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Fideos Spaguetti',
            brand='Carozzi',
            quantity=3,
            unit_price=890,
            is_purchased=True
        )
        ShoppingItem.objects.create(
            shopping_list=self.list1,
            name='Orégano',
            quantity=1,
            unit_price=0,
            has_unknown_price=True,
            is_purchased=False
        )

        client = Client()
        client.login(username='user1', password='password123')

        url = reverse('shopping:list_export_csv', kwargs={'pk': self.list1.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename=', response['Content-Disposition'])

        content = response.content.decode('utf-8')
        self.assertIn('Fideos Spaguetti', content)
        self.assertIn('Carozzi', content)
        self.assertIn('Orégano', content)
        self.assertIn('Sin precio', content)
        self.assertIn('TOTAL LISTA:', content)

        # Verificar que user2 no puede descargar CSV de user1
        client2 = Client()
        client2.login(username='user2', password='password123')
        forbidden_resp = client2.get(url)
        self.assertEqual(forbidden_resp.status_code, 404)

    def test_clear_purchased_items(self):
        """Verifica que solo se eliminen los productos marcados como comprados."""
        p1 = ShoppingItem.objects.create(shopping_list=self.list1, name='Manzana', quantity=1, unit_price=500, is_purchased=True)
        p2 = ShoppingItem.objects.create(shopping_list=self.list1, name='Naranja', quantity=1, unit_price=600, is_purchased=True)
        pending = ShoppingItem.objects.create(shopping_list=self.list1, name='Leche', quantity=2, unit_price=1100, is_purchased=False)

        client = Client()
        client.login(username='user1', password='password123')

        url = reverse('shopping:list_clear_purchased', kwargs={'pk': self.list1.pk})
        response = client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

        # p1 y p2 deben haber sido eliminados
        self.assertFalse(ShoppingItem.objects.filter(pk=p1.pk).exists())
        self.assertFalse(ShoppingItem.objects.filter(pk=p2.pk).exists())
        # pending debe seguir existiendo
        self.assertTrue(ShoppingItem.objects.filter(pk=pending.pk).exists())



class ShoppingItemValidationTests(TestCase):
    """
    Contrato de entrada del formulario de productos (Evaluación U2, criterio 2.1.3).

    - quantity: obligatoria, número entero entre 1 y 999 (ambos incluidos).
    - unit_price: opcional, número entero >= 0 en CLP. Vacío o 0 se registra como "sin precio".
    """

    def setUp(self):
        self.user = User.objects.create_user(username='validador', password='clave-de-prueba-123')
        self.shopping_list = ShoppingList.objects.create(user=self.user, name='Lista de pruebas')

    def build_form(self, **overrides):
        data = {'name': 'Leche Entera', 'brand': 'Marca Ficticia', 'category': 'LACTEOS',
                'quantity': '5', 'unit_price': '1350'}
        data.update(overrides)
        return ShoppingItemForm(data=data)

    # --- Campo quantity ---
    def test_cantidad_dentro_del_rango_aceptada(self):
        self.assertTrue(self.build_form(quantity='5').is_valid())

    def test_cantidad_bajo_el_minimo_rechazada(self):
        form = self.build_form(quantity='0')
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_cantidad_minimo_exacto_aceptada(self):
        self.assertTrue(self.build_form(quantity='1').is_valid())

    def test_cantidad_maximo_exacto_aceptada(self):
        self.assertTrue(self.build_form(quantity='999').is_valid())

    def test_cantidad_sobre_el_maximo_rechazada(self):
        form = self.build_form(quantity='1000')
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_cantidad_faltante_rechazada(self):
        form = self.build_form(quantity='')
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    # --- Campo unit_price (control existente, verificado con pruebas nuevas) ---
    def test_precio_legitimo_aceptado(self):
        form = self.build_form(unit_price='1350')
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['unit_price'], 1350)

    def test_precio_negativo_rechazado(self):
        form = self.build_form(unit_price='-5')
        self.assertFalse(form.is_valid())
        self.assertIn('unit_price', form.errors)

    def test_precio_no_numerico_rechazado(self):
        form = self.build_form(unit_price='abc')
        self.assertFalse(form.is_valid())
        self.assertIn('unit_price', form.errors)

    def test_precio_cero_frontera_queda_sin_precio(self):
        form = self.build_form(unit_price='0')
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save(commit=False).is_price_unknown)

    def test_precio_vacio_se_marca_sin_precio(self):
        form = self.build_form(unit_price='')
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['has_unknown_price'])
        self.assertEqual(form.cleaned_data['unit_price'], 0)

    # --- Backend: POST directo a las vistas, sin restricciones del navegador ---
    def test_backend_crear_con_cantidad_cero_no_guarda(self):
        self.client.force_login(self.user)
        url = reverse('shopping:item_create', kwargs={'list_pk': self.shopping_list.pk})
        response = self.client.post(url, {'name': 'Pan', 'quantity': '0', 'unit_price': '1000'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShoppingItem.objects.filter(name='Pan').exists())
        self.assertIn('Cantidad', ' '.join(str(m) for m in response.context['messages']))

    def test_backend_editar_con_cantidad_sobre_maximo_no_modifica(self):
        item = ShoppingItem.objects.create(shopping_list=self.shopping_list, name='Arroz', quantity=2, unit_price=1200)
        self.client.force_login(self.user)
        url = reverse('shopping:item_update', kwargs={'pk': item.pk})
        response = self.client.post(url, {'name': 'Arroz', 'quantity': '1000', 'unit_price': '1200'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('quantity', response.context['form'].errors)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)
