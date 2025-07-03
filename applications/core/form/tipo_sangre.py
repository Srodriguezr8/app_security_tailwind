import re
from django import forms
from django.forms import ModelForm

from applications.core.models import TipoSangre

class TipoSangreForm(ModelForm):
    class Meta:
        model = TipoSangre
        fields = [
            "tipo",
            "descripcion",
        ]
        error_messages = {
            "tipo": {  
                "unique": "Ya existe un tipo de sangre con este nombre.",
            },
        }
        widgets = {
            "tipo": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre del tipo de sangre",  
                "id": "id_nombre",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "descripcion": forms.Textarea(attrs={
                "placeholder": "Descripción opcional del tipo de sangre",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            })
        }
        labels = {
            "tipo": "Nombre del Tipo de Sangre",  
            "descripcion": "Descripción",

        }