import re
from django import forms
from django.forms import ModelForm

from applications.core.models import TipoMedicamento

class TipoMedicamentoForm(ModelForm):
    class Meta:
        model = TipoMedicamento
        fields = ["nombre", "descripcion", "activo"]
        error_messages = {
            "nombre": {  
                "unique": "Ya existe un tipo de medicamento con este nombre.",
            },
        }
        widgets = {
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre del tipo de medicamento",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "descripcion": forms.Textarea(attrs={
                "placeholder": "Descripción opcional del tipo de medicamento",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "rows": 3,
            }),
             "activo": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
            })
        }
        labels = {
            "nombre": "Nombre del Tipo de Medicamento",  
            "descripcion": "Descripción",
            "activo": "Activo"
        }