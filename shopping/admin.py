from django.contrib import admin
from django.utils.html import format_html
from .models import ShoppingList, ShoppingItem, Priority, Category


class ShoppingItemInline(admin.TabularInline):
    model = ShoppingItem
    extra = 1
    fields = ('name', 'brand', 'category', 'quantity', 'unit_price', 'has_unknown_price', 'is_purchased')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'priority_badge',
        'budget_limit_display',
        'total_amount_display',
        'items_count',
        'total_units',
        'created_at',
    )
    list_filter = ('priority', 'user', 'created_at')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    inlines = [ShoppingItemInline]
    ordering = ('priority', '-created_at')

    @admin.display(description='Prioridad')
    def priority_badge(self, obj):
        colors = {
            Priority.HIGH: ('#FEE2E2', '#991B1B', 'Alta 🔴'),
            Priority.MEDIUM: ('#FEF3C7', '#92400E', 'Media 🟡'),
            Priority.LOW: ('#D1FAE5', '#065F46', 'Baja 🟢'),
        }
        bg, fg, label = colors.get(obj.priority, ('#F1F5F9', '#334155', 'Normal'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; '
            'border-radius: 9999px; font-weight: 600; font-size: 0.8rem;">{}</span>',
            bg, fg, label
        )

    @admin.display(description='Presupuesto Máximo')
    def budget_limit_display(self, obj):
        if not obj.budget_limit:
            return "Sin tope"
        return f"${obj.budget_limit:,.0f} CLP".replace(",", ".")

    @admin.display(description='Total Estimado (CLP)')
    def total_amount_display(self, obj):
        return obj.formatted_total_amount


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'category_badge',
        'shopping_list',
        'quantity',
        'unit_price_display',
        'total_price_display',
        'is_purchased',
        'created_at',
    )
    list_filter = ('category', 'is_purchased', 'has_unknown_price', 'shopping_list__priority', 'shopping_list__user')
    search_fields = ('name', 'brand', 'shopping_list__name', 'shopping_list__user__username')
    ordering = ('-created_at',)

    @admin.display(description='Categoría')
    def category_badge(self, obj):
        return obj.get_category_display()

    @admin.display(description='Precio Unitario')
    def unit_price_display(self, obj):
        return obj.formatted_unit_price

    @admin.display(description='Subtotal Producto')
    def total_price_display(self, obj):
        return obj.formatted_total_price
