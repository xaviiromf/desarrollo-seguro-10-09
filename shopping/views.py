from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import ShoppingList, ShoppingItem, Priority
from .forms import (
    ShoppingListForm,
    ShoppingItemForm,
    UserRegistrationForm,
    UserLoginForm,
)


# ==========================================
# Autenticación basada en CBV
# ==========================================

class UserLoginView(LoginView):
    """Vista CBV para inicio de sesión de usuarios."""
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"¡Bienvenido(a) de nuevo, {form.get_user().username}!")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Vista CBV para cerrar sesión."""
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión exitosamente.")
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    """Vista CBV para el registro de nuevos usuarios."""
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('shopping:list_index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shopping:list_index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"¡Cuenta creada con éxito! Bienvenido(a) {user.username}.")
        return redirect(self.success_url)


# ==========================================
# Listas de Compras (CBVs)
# ==========================================

class ShoppingListListView(LoginRequiredMixin, ListView):
    """
    Vista separada de 'Listado de Listas de Compras'.
    Permite al usuario ver todas sus listas, filtradas y ordenadas por prioridad o fecha.
    """
    model = ShoppingList
    template_name = 'shopping/shoppinglist_list.html'
    context_object_name = 'shopping_lists'
    paginate_by = 12

    def get_queryset(self):
        # Aislamiento estricto por usuario logueado
        queryset = ShoppingList.objects.filter(user=self.request.user).prefetch_related('items')

        # Ordenamiento
        sort_by = self.request.GET.get('sort', 'priority')
        if sort_by == 'priority':
            # 1: Alta, 2: Media, 3: Baja
            queryset = queryset.order_by('priority', '-created_at')
        elif sort_by == '-priority':
            queryset = queryset.order_by('-priority', '-created_at')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')

        # Filtro de búsqueda opcional
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_lists = ShoppingList.objects.filter(user=self.request.user).prefetch_related('items')
        
        # Estadísticas resumidas para el usuario
        grand_total = sum(item.total_price for s_list in user_lists for item in s_list.items.all())
        total_items = sum(item.quantity for s_list in user_lists for item in s_list.items.all())

        context.update({
            'current_sort': self.request.GET.get('sort', 'priority'),
            'search_query': self.request.GET.get('q', ''),
            'total_lists_count': user_lists.count(),
            'grand_projected_total': grand_total,
            'total_units_all_lists': total_items,
            'priority_choices': Priority.choices,
        })
        return context


class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    """
    Vista separada de 'Detalle de la Lista de Compras'.
    Muestra los productos de la lista específica, cálculos de subtotales por producto,
    total general de la lista y formulario para agregar nuevos productos.
    """
    model = ShoppingList
    template_name = 'shopping/shoppinglist_detail.html'
    context_object_name = 'shopping_list'

    def get_queryset(self):
        # Asegurar que el usuario solo acceda a sus propias listas
        return ShoppingList.objects.filter(user=self.request.user).prefetch_related('items')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Instanciar el formulario para agregar productos directamente en el detalle
        context['item_form'] = ShoppingItemForm()
        # Lista ordenada de ítems
        context['items'] = self.object.items.all().order_by('is_purchased', '-created_at')
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """Crea una nueva lista de compras para el usuario logueado."""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping/shoppinglist_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f"¡Lista '{form.instance.name}' creada exitosamente!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shopping:list_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_title'] = 'Crear Nueva Lista de Compras'
        context['button_label'] = 'Guardar Lista'
        return context


class ShoppingListUpdateView(LoginRequiredMixin, UpdateView):
    """Edita una lista de compras existente del usuario logueado."""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping/shoppinglist_form.html'

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"¡Lista '{form.instance.name}' actualizada!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shopping:list_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_title'] = f"Editar Lista: {self.object.name}"
        context['button_label'] = 'Guardar Cambios'
        return context


class ShoppingListDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina una lista de compras del usuario logueado."""
    model = ShoppingList
    template_name = 'shopping/shoppinglist_confirm_delete.html'
    success_url = reverse_lazy('shopping:list_index')

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Lista de compras eliminada correctamente.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# Ítems / Productos de Compras (CBVs)
# ==========================================

class ShoppingItemCreateView(LoginRequiredMixin, CreateView):
    """Agrega un producto a una lista de compras específica."""
    model = ShoppingItem
    form_class = ShoppingItemForm

    def form_valid(self, form):
        list_pk = self.kwargs.get('list_pk')
        shopping_list = get_object_or_404(ShoppingList, pk=list_pk, user=self.request.user)
        form.instance.shopping_list = shopping_list
        item = form.save()
        messages.success(
            self.request,
            f"Producto '{item.name}' agregado a la lista. Subtotal: ${item.total_price:,.2f}"
        )
        return redirect('shopping:list_detail', pk=shopping_list.pk)

    def form_invalid(self, form):
        list_pk = self.kwargs.get('list_pk')
        messages.error(self.request, "Por favor verifica los datos del producto ingresado.")
        return redirect('shopping:list_detail', pk=list_pk)


class ShoppingItemUpdateView(LoginRequiredMixin, UpdateView):
    """Edita un producto existente dentro de una lista de compras."""
    model = ShoppingItem
    form_class = ShoppingItemForm
    template_name = 'shopping/shoppingitem_form.html'

    def get_queryset(self):
        return ShoppingItem.objects.filter(shopping_list__user=self.request.user)

    def form_valid(self, form):
        item = form.save()
        messages.success(self.request, f"Producto '{item.name}' actualizado.")
        return redirect('shopping:list_detail', pk=item.shopping_list.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping_list'] = self.object.shopping_list
        return context


class ShoppingItemDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un producto de una lista."""
    model = ShoppingItem

    def get_queryset(self):
        return ShoppingItem.objects.filter(shopping_list__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        list_pk = item.shopping_list.pk
        item_name = item.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Producto '{item_name}' eliminado de la lista.")
        return response

    def get_success_url(self):
        return reverse('shopping:list_detail', kwargs={'pk': self.object.shopping_list.pk})


class ShoppingItemTogglePurchasedView(LoginRequiredMixin, View):
    """Alterna el estado 'comprado' de un producto de manera reactiva."""
    def post(self, request, pk, *args, **kwargs):
        item = get_object_or_404(ShoppingItem, pk=pk, shopping_list__user=request.user)
        item.is_purchased = not item.is_purchased
        item.save()

        # Respuesta AJAX o redirección estándar
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_purchased': item.is_purchased,
                'item_id': item.id,
                'list_total': str(item.shopping_list.total_amount),
            })

        return redirect('shopping:list_detail', pk=item.shopping_list.pk)
