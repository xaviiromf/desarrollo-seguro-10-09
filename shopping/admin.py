from django.contrib import admin
from django.utils.html import format_html
from .models import ShoppingList, ShoppingItem, Priority


class ShoppingItemInline(admin.TabularInline):
    model = ShoppingItem
    extra = 1
    fields = ('name', 'brand', 'quantity', 'unit_price', 'is_purchased')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'priority_badge',
        'total_amount_display',
        'total_units',
        'items_count',
        'created_at',
    )
    list_filter = ('priority', 'user', 'created_at')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    inlines = [ShoppingItemInline]
    ordering = ('priority', '-created_at')

    @admin.display(description='Prioridad')
    def priority_badge(self, obj):
        colors = {
            Priority.HIGH: ('#FFB4A2', '#6D2B23', 'Alta 🔴'),
            Priority.MEDIUM: ('#FFE5B4', '#7D5A1E', 'Media 🟡'),
            Priority.LOW: ('#D8E2DC', '#2B5844', 'Baja 🟢'),
        }
        bg, fg, label = colors.get(obj.priority, ('#E2E8F0', '#334155', 'Normal'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; '
            'border-radius: 9999px; font-weight: 600; font-size: 0.8rem;">{}</span>',
            bg, fg, label
        )

    @admin.display(description='Total Lista ($)')
    def total_amount_display(self, obj):
        return f"${obj.total_amount:,.2f}"


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'shopping_list',
        'quantity',
        'unit_price_display',
        'total_price_display',
        'is_purchased',
        'created_at',
    )
    list_filter = ('is_purchased', 'shopping_list__priority', 'shopping_list__user')
    search_fields = ('name', 'brand', 'shopping_list__name', 'shopping_list__user__username')
    ordering = ('-created_at',)

    @admin.display(description='Precio Unitario')
    def unit_price_display(self, obj):
        return f"${obj.unit_price:,.2f}"

    @admin.display(description='Subtotal Producto')
    def total_price_display(self, obj):
        return f"${obj.total_price:,.2f}"
