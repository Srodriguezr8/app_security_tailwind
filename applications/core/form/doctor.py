import re
from django import forms
from django.forms import ModelForm
from django.forms import ClearableFileInput

from applications.core.models import Doctor

class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "nombres",
            "apellidos",
            "ruc",
            "fecha_nacimiento",
            "direccion",
            "latitud",
            "longitud",
            "codigo_unico_doctor",
            "especialidad",
            "telefonos",
            "email",
            "horario_atencion",
            "duracion_atencion",
            "curriculum",
            "firma_digital",
            "foto",
            "imagen_receta",
            "activo"
           
        ]
        error_messages = {
            "ruc": {
                "unique": "Ya existe un doctor con este RUC.",
            },
        }
        widgets = {
    "nombres": forms.TextInput(attrs={
        "placeholder": "Ingrese los nombres del doctor",
        "id": "id_nombres",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    }),
    "apellidos": forms.TextInput(attrs={
        "placeholder": "Ingrese los apellidos del doctor",
        "id": "id_apellidos",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    }),
    "ruc": forms.TextInput(attrs={
        "placeholder": "Ingrese RUC del doctor",
        "id": "id_ruc",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        "maxlength": "13",
    }),
    "fecha_nacimiento": forms.DateInput(attrs={
        "type": "date",
        "id": "id_fecha_nacimiento",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    },
    format="%Y-%m-%d"),
    "direccion": forms.TextInput(attrs={
        "placeholder": "Ingrese dirección de trabajo del doctor",
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
    "codigo_unico_doctor": forms.TextInput(attrs={
        "placeholder": "Código único del doctor",
        "id": "id_codigo_unico_doctor",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        "maxlength": "20",
    }),
    "especialidad": forms.SelectMultiple(attrs={
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
    }),
    "telefonos": forms.TextInput(attrs={
        "placeholder": "Número de teléfono del doctor",
        "id": "id_telefonos",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        "maxlength": "20",
    }),
    "email": forms.EmailInput(attrs={
        "placeholder": "Correo electrónico del doctor (opcional)",
        "id": "id_email",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    }),
    "horario_atencion": forms.Textarea(attrs={
        "placeholder": "Ejemplo: Lunes a Viernes, 08h00 - 13h00",
        "id": "id_horario_atencion",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        "rows": 3,
    }),
    "duracion_atencion": forms.NumberInput(attrs={
        "placeholder": "Duración en minutos",
        "id": "id_duracion_atencion",
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        "min": "1",
        "max": "480",
    }),
    "curriculum": forms.FileInput(attrs={
        "id": "id_curriculum",
        "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400",
        "accept": ".pdf,.doc,.docx",
    }),
    "firma_digital": forms.FileInput(attrs={
        "id": "id_firma_digital",
        "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400",
        "accept": "image/*",
    }),
    "foto": forms.FileInput(attrs={
        "id": "id_foto",
        "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400",
        "accept": "image/*",
    }),
    "imagen_receta": forms.FileInput(attrs={
        "id": "id_imagen_receta",
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
    "ruc": "RUC",
    "fecha_nacimiento": "Fecha de Nacimiento",
    "direccion": "Dirección de Trabajo",
    "latitud": "Latitud",
    "longitud": "Longitud",
    "codigo_unico_doctor": "Código Único del Doctor",
    "especialidad": "Especialidades",
    "telefonos": "Teléfonos",
    "email": "Correo Electrónico",
    "horario_atencion": "Horario de Atención",
    "duracion_atencion": "Duración de Cita (minutos)",
    "curriculum": "Currículum Vitae",
    "firma_digital": "Firma Digital",
    "foto": "Foto",
    "imagen_receta": "Imagen para Recetas",
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