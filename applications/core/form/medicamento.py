import re
from django import forms
from django.forms import ModelForm
from applications.core.models import Medicamento, TipoMedicamento, MarcaMedicamento, ViaAdministracion

class MedicamentoForm(ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            "tipo",
            "marca_medicamento",
            "nombre",
            "descripcion",
            "concentracion",
            "via_administracion",
            "cantidad",
            "precio",
            "comercial",
            "foto",
            "activo"
        ]

        error_messages = {
            "nombre": {
                "unique": "Ya existe un medicamento con este nombre.",
            },
        }
        
        widgets = {
            "tipo": forms.Select(attrs={
                "id": "id_tipo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "marca_medicamento": forms.Select(attrs={
                "id": "id_marca_medicamento",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "nombre": forms.TextInput(attrs={
                "placeholder": "Ingrese el nombre del medicamento",
                "id": "id_nombre",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "descripcion": forms.Textarea(attrs={
                "placeholder": "Descripción, uso y precauciones",
                "id": "id_descripcion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "concentracion": forms.TextInput(attrs={
                "placeholder": "Ejemplo: 500mg, 1g, 5%",
                "id": "id_concentracion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "via_administracion": forms.Select(attrs={
                "id": "id_via_administracion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "choices": ViaAdministracion.choices,
            }),
            "cantidad": forms.NumberInput(attrs={
                "placeholder": "Cantidad en stock",
                "id": "id_cantidad",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "min": "0",
            }),
            "precio": forms.NumberInput(attrs={
                "placeholder": "Precio unitario",
                "id": "id_precio",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.01",
                "min": "0",
            }),
            "comercial": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
            }),
            "foto": forms.FileInput(attrs={
                "id": "id_foto",
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400",
                "accept": "image/*",
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
            })
        }

        labels = {
            "tipo": "Tipo de Medicamento",
            "marca_medicamento": "Marca",
            "nombre": "Nombre del Medicamento",
            "descripcion": "Descripción",
            "concentracion": "Concentración",
            "via_administracion": "Vía de Administración",
            "cantidad": "Stock Disponible",
            "precio": "Precio Unitario",
            "comercial": "Medicamento Comercial",
            "foto": "Foto del Medicamento",
            "activo": "Activo"
        }

    @property
    def id(self):
        return self.instance.pk if self.instance else None

   