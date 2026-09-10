from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class Priority(models.IntegerChoices):
    HIGH = 1, 'Alta'
    MEDIUM = 2, 'Media'
    LOW = 3, 'Baja'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Usuario'
    )
    name = models.CharField(max_length=150, verbose_name='Nombre de la Lista')
    description = models.TextField(blank=True, verbose_name='Descripción / Notas')
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name='Prioridad'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        verbose_name = 'Lista de Compras'
        verbose_name_plural = 'Listas de Compras'
        ordering = ['priority', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"

    @property
    def total_amount(self) -> Decimal:
        """Calcula el total acumulado de todos los productos en la lista."""
        total = sum(item.total_price for item in self.items.all())
        return Decimal(str(total)).quantize(Decimal('0.01'))

    @property
    def total_units(self) -> int:
        """Suma total de unidades físicas de todos los productos."""
        return sum(item.quantity for item in self.items.all())

    @property
    def items_count(self) -> int:
        """Cantidad de productos distintos en la lista."""
        return self.items.count()

    @property
    def priority_badge_class(self) -> str:
        """Clase CSS correspondiente para el estilo pastel."""
        badge_classes = {
            Priority.HIGH: 'badge-priority-high',
            Priority.MEDIUM: 'badge-priority-medium',
            Priority.LOW: 'badge-priority-low',
        }
        return badge_classes.get(self.priority, 'badge-priority-medium')


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Lista de Compras'
    )
    name = models.CharField(max_length=200, verbose_name='Producto')
    brand = models.CharField(max_length=150, blank=True, verbose_name='Marca')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Precio por Unidad ($)'
    )
    is_purchased = models.BooleanField(default=False, verbose_name='¿Comprado?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha agregado')

    class Meta:
        verbose_name = 'Producto de Lista'
        verbose_name_plural = 'Productos de Lista'
        ordering = ['is_purchased', '-created_at']

    def __str__(self):
        brand_str = f" [{self.brand}]" if self.brand else ""
        return f"{self.name}{brand_str} x{self.quantity}"

    @property
    def total_price(self) -> Decimal:
        """Calcula el total por producto: cantidad * precio por unidad."""
        total = Decimal(self.quantity) * self.unit_price
        return total.quantize(Decimal('0.01'))
