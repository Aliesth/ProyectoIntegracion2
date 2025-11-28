# aplicacion/forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Rol, Fruta, Contrato

class RegistroForm(UserCreationForm):
    # Añadimos el campo email requerido
    email = forms.EmailField(
        required=True,
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com', 'class': 'form-control'})
    )
    
    # Campo Rol (usamos los choices del modelo)
    rolReg = forms.ChoiceField(
        choices=Rol.choices,
        required=True,
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Campo Nombre Completo (es opcional ya que no está en el modelo User)
    nombre = forms.CharField(
        required=False,
        label='Nombre Completo',
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Juan Pérez', 'class': 'form-control'})
    )
    
    class Meta(UserCreationForm.Meta):
        # Aseguramos que el campo 'password2' esté incluido para la confirmación
        fields = UserCreationForm.Meta.fields + ('email', 'rolReg', 'nombre')
        
        # Aplicamos estilos de Bootstrap a los campos por defecto
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ingrese un usuario', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Cree una contraseña', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirme su contraseña', 'class': 'form-control'}),
        }

class FrutaForm(forms.ModelForm):
    # Opcional: Puedes personalizar campos si lo necesitas
    # nombre = forms.CharField(label='Nombre de la Fruta', max_length=300)

    class Meta:
        model = Fruta
        # Incluye todos los campos excepto 'id' (que es automático)
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'marca']
        # Opcional: Etiquetas personalizadas para los campos
        labels = {
            'nombre': 'Nombre de la Fruta',
            'descripcion': 'Descripción Detallada',
            'precio': 'Precio Unitario ($)',
            'stock': 'Cantidad en Stock',
            'marca': 'Marca / Origen',
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['nombre_transporte', 'fecha_inicio', 'fecha_termino']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre_transporte': forms.TextInput(attrs={'class': 'form-control'}),
        }
