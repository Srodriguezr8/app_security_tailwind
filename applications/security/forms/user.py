import re
from django import forms
from django.forms import ModelForm
from applications.security.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "dni",
            "email",
            "first_name",
            "last_name",
            "is_active",
        ]

        widgets = {
            "dni": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "first_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
            }),
        }

        labels = {
            "dni": "Documento de Identidad",
            "email": "Correo Electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "is_active": "¿Activo?",
         
        }
        
        

class UserStatusForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 rounded focus:ring-blue-500'
            }),
        }
        labels = {
            'is_active': '¿Está activo?',
        }        