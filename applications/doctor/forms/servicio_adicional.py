import re
from django import forms
from django.forms import ModelForm
from applications.doctor.models import ServiciosAdicionales

class ServicioAdicionalForm(ModelForm):
    class Meta:
        model = ServiciosAdicionales
        fields = [
            "nombre_servicio",
            "costo_servicio",
            "descripcion",
            "activo"
        ]
    
        widgets = {
            "nombre_servicio": forms.TextInput(attrs={
                "placeholder": "Ej: Radiografía, Laboratorio clínico...",  
                "id": "id_nombre_servicio",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "costo_servicio": forms.NumberInput(attrs={
                "placeholder": "Ej: 25.00",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.01",
                "min": "0"
            }),
            "descripcion": forms.Textarea(attrs={
                "placeholder": "Descripción opcional del servicio...",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
            })
        }
        labels = {
            "nombre_servicio": "Nombre del Servicio",  
            "costo_servicio": "Costo del Servicio ($)",
            "descripcion": "Descripción",
            "activo": "Activo"
        }