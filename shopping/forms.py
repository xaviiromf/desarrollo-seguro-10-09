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
    class Meta:
        model = ShoppingItem
        fields = ['name', 'brand', 'quantity', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del producto'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Marca (opcional)'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'step': 1, 'id': 'id_quantity'}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'id': 'id_unit_price'}),
        }


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
