import re
from django import forms
from django.forms import ModelForm

from applications.core.models import Diagnostico

class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = [
            "codigo",
            "descripcion",
            "datos_adicionales",
            "activo"
        ]
        error_messages = {
            "codigo": {
                "unique": "Ya existe un diagnóstico con este código.",
            },
        }
        widgets = {
            "codigo": forms.TextInput(attrs={
                "placeholder": "Ingrese código del diagnóstico",
                "id": "id_name",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "descripcion": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre del diagnóstico",
                "id": "id_name",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "datos_adicionales": forms.Textarea(attrs={
                "placeholder": "Datos adiciones opcional del diagnóstico",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
            })
        }
        labels = {
            "codigo": "Código",
            "descripcion": "Descripción",
            "datos_adicionales": "Datos Adicionales",
            "activo": "Activo"
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
    
    def clean_icon(self):
        icon = self.cleaned_data['icon']
        if not icon:
            raise forms.ValidationError("El campo ícono es requerido.")
        
        # Patrones para FontAwesome v5 y v6
        patterns = [
            r'^(fas|far|fal|fad|fab|fa)\s+fa-\w+',      # fas fa-user (v5)
            r'^fa-(solid|regular|light|duotone|brands)\s+fa-\w+',  # fa-solid fa-user (v6)
            r'^fa-\w+$',                                 # fa-user (formato simple)
        ]
        
        is_valid = any(re.match(pattern, icon) for pattern in patterns)
        
        if not is_valid:
            raise forms.ValidationError(
                "Formato de ícono inválido. Ejemplos válidos: "
                "'fas fa-user', 'fa-solid fa-person', 'fa-home'"
            )
        
        return icon