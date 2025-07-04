import re
from django import forms
from django.forms import ModelForm

from applications.core.models import FotoPaciente

class FotoPacienteForm(ModelForm):
    class Meta:
        model = FotoPaciente
        fields = [
            "paciente",
            "imagen",
            "descripcion"
        ]
        
        widgets = {
            "paciente": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "imagen": forms.FileInput(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "accept": "image/*",
            }),
            "descripcion": forms.Textarea(attrs={
                "placeholder": "Comentario opcional sobre la imagen (ej. cicatriz, antes/después, etc.)",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
        }
        
        labels = {
            "paciente": "Paciente",
            "imagen": "Imagen del Paciente",
            "descripcion": "Descripción"
        }
    
    @property
    def id(self):
        return self.instance.pk if self.instance else None