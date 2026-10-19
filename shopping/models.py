from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User

# Regla de negocio: cantidad por producto entre 1 y 999 unidades (validada en el servidor).
QUANTITY_MIN = 1
QUANTITY_MAX = 999


class Priority(models.IntegerChoices):
    HIGH = 1, 'Alta'
    MEDIUM = 2, 'Media'
    LOW = 3, 'Baja'


class Category(models.TextChoices):
    DAIRY = 'LACTEOS', '🥛 Lácteos y Huevos'
    FRUITS_VEGGIES = 'VERDURAS', '🍎 Frutas y Verduras'
    MEAT = 'CARNES', '🥩 Carnes y Pescados'
    BAKERY = 'PANADERIA', '🍞 Panadería y Pastelería'
    PANTRY = 'DESPENSA', '🌾 Abarrotes y Despensa'
    BEVERAGES = 'BEBIDAS', '🧃 Bebidas y Jugos'
    CLEANING = 'LIMPIEZA', '🧼 Limpieza y Aseo'
    FROZEN = 'CONGELADOS', '🧊 Congelados'
    SNACKS = 'SNACKS', '🍫 Snacks y Golosinas'
    OTHER = 'OTRO', '📦 Otro'


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
    budget_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Presupuesto Máximo (CLP $)'
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
    def total_amount(self) -> int:
        """Calcula el total acumulado en Pesos Chilenos (CLP)."""
        return sum(item.total_price for item in self.items.all())

    @property
    def formatted_total_amount(self) -> str:
        """Formatea el total en Pesos Chilenos con separador de miles: $12.990."""
        return f"${self.total_amount:,.0f}".replace(",", ".")

    @property
    def total_units(self) -> int:
        """Suma total de unidades físicas de todos los productos."""
        return sum(item.quantity for item in self.items.all())

    @property
    def items_count(self) -> int:
        """Cantidad de productos distintos en la lista."""
        return self.items.count()

    @property
    def items_without_price_count(self) -> int:
        """Cuenta cuántos productos no tienen precio definido."""
        return self.items.filter(
            models.Q(has_unknown_price=True) | models.Q(unit_price__isnull=True) | models.Q(unit_price=0)
        ).count()

    @property
    def has_items_without_price(self) -> bool:
        """Indica si la lista contiene productos sin precio."""
        return self.items_without_price_count > 0

    @property
    def purchased_items_count(self) -> int:
        """Cantidad de productos ya marcados como comprados."""
        return self.items.filter(is_purchased=True).count()

    @property
    def purchased_total_amount(self) -> int:
        """Total gastado en productos ya comprados."""
        return sum(item.total_price for item in self.items.filter(is_purchased=True))

    @property
    def pending_total_amount(self) -> int:
        """Total restante por gastar en productos pendientes."""
        return sum(item.total_price for item in self.items.filter(is_purchased=False))

    @property
    def completion_percentage(self) -> int:
        """Porcentaje de productos comprados respecto al total."""
        total = self.items_count
        if total == 0:
            return 0
        return int((self.purchased_items_count / total) * 100)

    @property
    def budget_percentage(self) -> int | None:
        """Porcentaje del presupuesto consumido."""
        if not self.budget_limit or self.budget_limit == 0:
            return None
        return int(round((self.total_amount / self.budget_limit) * 100))


    @property
    def is_over_budget(self) -> bool:
        """Retorna True si el total estimado supera el presupuesto máximo asignado."""
        if not self.budget_limit:
            return False
        return self.total_amount > self.budget_limit

    @property
    def remaining_budget(self) -> int | None:
        """Monto restante del presupuesto (puede ser negativo si hay exceso)."""
        if not self.budget_limit:
            return None
        return self.budget_limit - self.total_amount

    @property
    def priority_badge_class(self) -> str:
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
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.PANTRY,
        verbose_name='Categoría'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(QUANTITY_MIN, message=f'La cantidad mínima es {QUANTITY_MIN}.'),
            MaxValueValidator(QUANTITY_MAX, message=f'La cantidad máxima es {QUANTITY_MAX}.'),
        ],
        verbose_name='Cantidad'
    )
    unit_price = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name='Precio por Unidad (CLP $)'
    )
    has_unknown_price = models.BooleanField(
        default=False,
        verbose_name='¿Sin precio definido aún?'
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
    def is_price_unknown(self) -> bool:
        """Retorna True si el producto no tiene precio o se marcó como desconocido."""
        return self.has_unknown_price or self.unit_price is None or self.unit_price == 0

    @property
    def total_price(self) -> int:
        """Calcula el total por producto: cantidad * precio unitario (o 0 si sin precio)."""
        if self.is_price_unknown:
            return 0
        return int(self.quantity * self.unit_price)

    @property
    def formatted_unit_price(self) -> str:
        """Formatea el precio unitario en Pesos Chilenos."""
        if self.is_price_unknown:
            return "Sin precio"
        return f"${self.unit_price:,.0f}".replace(",", ".")

    @property
    def formatted_total_price(self) -> str:
        """Formatea el subtotal en Pesos Chilenos."""
        if self.is_price_unknown:
            return "Sin precio"
        return f"${self.total_price:,.0f}".replace(",", ".")
