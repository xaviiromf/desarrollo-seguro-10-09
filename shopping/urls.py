from django.urls import path
from .views import (
    ShoppingListListView,
    ShoppingListDetailView,
    ShoppingListCreateView,
    ShoppingListUpdateView,
    ShoppingListDeleteView,
    ShoppingListDuplicateView,
    ShoppingListBulkToggleView,
    ShoppingListExportCSVView,
    ShoppingListClearPurchasedView,
    ShoppingItemCreateView,
    ShoppingItemUpdateView,
    ShoppingItemDeleteView,
    ShoppingItemTogglePurchasedView,
)

app_name = 'shopping'

urlpatterns = [
    # Vistas de Listas de Compras
    path('', ShoppingListListView.as_view(), name='list_index'),
    path('lists/new/', ShoppingListCreateView.as_view(), name='list_create'),
    path('lists/<int:pk>/', ShoppingListDetailView.as_view(), name='list_detail'),
    path('lists/<int:pk>/edit/', ShoppingListUpdateView.as_view(), name='list_update'),
    path('lists/<int:pk>/delete/', ShoppingListDeleteView.as_view(), name='list_delete'),
    path('lists/<int:pk>/duplicate/', ShoppingListDuplicateView.as_view(), name='list_duplicate'),
    path('lists/<int:pk>/bulk-toggle/', ShoppingListBulkToggleView.as_view(), name='list_bulk_toggle'),
    path('lists/<int:pk>/export-csv/', ShoppingListExportCSVView.as_view(), name='list_export_csv'),
    path('lists/<int:pk>/clear-purchased/', ShoppingListClearPurchasedView.as_view(), name='list_clear_purchased'),



    # Vistas de Ítems / Productos
    path('lists/<int:list_pk>/items/add/', ShoppingItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/edit/', ShoppingItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', ShoppingItemDeleteView.as_view(), name='item_delete'),
    path('items/<int:pk>/toggle/', ShoppingItemTogglePurchasedView.as_view(), name='item_toggle'),
]
