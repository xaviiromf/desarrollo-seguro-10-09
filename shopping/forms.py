from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ShoppingList, ShoppingItem


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'priority', 'budget_limit', 'description']
        labels = {
            'name': 'Nombre de la Lista',
            'priority': 'Prioridad',
            'budget_limit': 'Presupuesto Máximo (CLP $, opcional)',
            'description': 'Descripción o notas (opcional)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Compras del Mes, Verdulería...'}),
            'budget_limit': forms.NumberInput(attrs={'min': 0, 'step': 1000, 'placeholder': 'Ej. 50000'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notas adicionales, supermercado de preferencia...'}),
        }


class ShoppingItemForm(forms.ModelForm):
    has_unknown_price = forms.BooleanField(
        required=False,
        label="¿Sin precio definido?",
        help_text="Marca esta casilla si aún no conoces el precio del producto.",
        widget=forms.CheckboxInput(attrs={'id': 'id_has_unknown_price'})
    )

    class Meta:
        model = ShoppingItem
        fields = ['name', 'brand', 'category', 'quantity', 'unit_price', 'has_unknown_price']
        labels = {
            'name': 'Producto',
            'brand': 'Marca (opcional)',
            'category': 'Categoría',
            'quantity': 'Cantidad',
            'unit_price': 'Precio por unidad (CLP $)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Leche Entera, Manzanas...'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Ej. Colun, Soprole...'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'step': 1, 'id': 'id_quantity'}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': 1, 'id': 'id_unit_price', 'placeholder': 'Ej. 1350'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.fields:
            self.fields['category'].required = False

    def clean(self):
        from .models import Category
        cleaned_data = super().clean()
        has_unknown_price = cleaned_data.get('has_unknown_price')
        unit_price = cleaned_data.get('unit_price')
        if not cleaned_data.get('category'):
            cleaned_data['category'] = Category.PANTRY
        if has_unknown_price:
            cleaned_data['unit_price'] = 0
        elif unit_price is None:
            cleaned_data['unit_price'] = 0
            cleaned_data['has_unknown_price'] = True
        return cleaned_data




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Tu usuario'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Tu contraseña'})
