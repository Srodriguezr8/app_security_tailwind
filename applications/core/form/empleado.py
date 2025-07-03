import re
from django import forms
from django.forms import ModelForm

from applications.core.models import Empleado

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = [
            "nombres",
            "apellidos",
            "cedula_ecuatoriana",
            "dni",
            "fecha_nacimiento",
            "cargo",
            "sueldo",
            "fecha_ingreso",
            "direccion",
            "latitud",
            "longitud",
            "foto",
            "activo"           
        ]
        
        widgets = {
            "nombres": forms.TextInput(attrs={
                "placeholder": "Ingrese los nombres del empleado",
                "id": "id_nombres",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "apellidos": forms.TextInput(attrs={
                "placeholder": "Ingrese los apellidos del empleado",
                "id": "id_apellidos",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "cedula_ecuatoriana": forms.TextInput(attrs={
                "placeholder": "Ingrese la cédula ecuatoriana",
                "id": "id_cedula_ecuatoriana",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "maxlength": "10",
            }),
            "dni": forms.TextInput(attrs={
                "placeholder": "Ingrese DNI internacional (opcional)",
                "id": "id_dni",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "maxlength": "30",
            }),
            "fecha_nacimiento": forms.DateInput(attrs={
                "type": "date",
                "id": "id_fecha_nacimiento",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            },
            format="%Y-%m-%d"),
            "cargo": forms.Select(attrs={
                "id": "id_cargo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "sueldo": forms.NumberInput(attrs={
                "placeholder": "Ingrese el sueldo",
                "id": "id_sueldo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.01",
                "min": "0",
            }),
            "fecha_ingreso": forms.DateInput(attrs={
                "type": "date",
                "id": "id_fecha_ingreso",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            },
            format="%Y-%m-%d"),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Ingrese dirección del empleado",
                "id": "id_direccion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "latitud": forms.NumberInput(attrs={
                "placeholder": "Coordenada de latitud (opcional)",
                "id": "id_latitud",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.000001",
            }),
            "longitud": forms.NumberInput(attrs={
                "placeholder": "Coordenada de longitud (opcional)",
                "id": "id_longitud",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "step": "0.000001",
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
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "cedula_ecuatoriana": "Cédula Ecuatoriana",
            "dni": "DNI Internacional",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "cargo": "Cargo",
            "sueldo": "Sueldo",
            "fecha_ingreso": "Fecha de Ingreso",
            "direccion": "Dirección",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "foto": "Foto del Empleado",
            "activo": "Activo"
        }
    @property
    def id(self):
        return self.instance.pk if self.instance else None

    