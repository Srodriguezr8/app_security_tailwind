import re
from django import forms
from django.forms import ModelForm
from django.utils import timezone
from applications.core.models import GastoMensual, TipoGasto

class GastoMensualForm(ModelForm):
    class Meta:
        model = GastoMensual
        fields = [
            "tipo_gasto",
            "fecha",
            "valor",
            "observacion"
        ]
        
        widgets = {
            "tipo_gasto": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "fecha": forms.DateInput(attrs={
                "type": "date",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "value": timezone.now().strftime('%Y-%m-%d'),
            },
            format="%Y-%m-%d"),
            "valor": forms.NumberInput(attrs={
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "observacion": forms.Textarea(attrs={
                "placeholder": "Observación adicional sobre este gasto (opcional)",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            })
        }
        labels = {
            "tipo_gasto": "Tipo de Gasto",
            "fecha": "Fecha del Gasto",
            "valor": "Valor ($)",
            "observacion": "Observación"
        }
