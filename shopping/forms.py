from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ShoppingList, ShoppingItem


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'priority', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre de la lista'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción o notas opcionales'}),
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
        fields = ['name', 'brand', 'quantity', 'unit_price', 'has_unknown_price']
        labels = {
            'name': 'Producto',
            'brand': 'Marca (opcional)',
            'quantity': 'Cantidad',
            'unit_price': 'Precio por unidad (CLP $)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Leche Entera, Manzanas...'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Ej. Colun, Soprole...'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'step': 1, 'id': 'id_quantity'}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': 1, 'id': 'id_unit_price', 'placeholder': 'Ej. 1350'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        has_unknown_price = cleaned_data.get('has_unknown_price')
        unit_price = cleaned_data.get('unit_price')
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
