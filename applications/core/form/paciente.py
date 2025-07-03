import re
from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator

from applications.core.models import Paciente, TipoSangre
from applications.core.utils.paciente import EstadoCivilChoices, SexoChoices

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombres",
            "apellidos",
            "cedula_ecuatoriana",
            "dni",
            "fecha_nacimiento",
            "telefono",
            "email",
            "sexo",
            "estado_civil",
            "direccion",
            "latitud",
            "longitud",
            "tipo_sangre",
            "foto",
            "antecedentes_personales",
            "antecedentes_quirurgicos",
            "antecedentes_familiares",
            "alergias",
            "medicamentos_actuales",
            "habitos_toxicos",
            "vacunas",
            "antecedentes_gineco_obstetricos",
            "activo"           
        ]
        
        widgets = {
            "nombres": forms.TextInput(attrs={
                "placeholder": "Ingrese los nombres del paciente",
                "id": "id_nombres",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "apellidos": forms.TextInput(attrs={
                "placeholder": "Ingrese los apellidos del paciente",
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
            "telefono": forms.TextInput(attrs={
                "placeholder": "Ingrese teléfono(s) separados por comas",
                "id": "id_telefono",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "maxlength": "50",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Ingrese el correo electrónico (opcional)",
                "id": "id_email",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "sexo": forms.Select(attrs={
                "id": "id_sexo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "estado_civil": forms.Select(attrs={
                "id": "id_estado_civil",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "direccion": forms.TextInput(attrs={
                "placeholder": "Ingrese dirección domiciliaria",
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
            "tipo_sangre": forms.Select(attrs={
                "id": "id_tipo_sangre",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }),
            "foto": forms.FileInput(attrs={
                "id": "id_foto",
                "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400",
                "accept": "image/*",
            }),
            "antecedentes_personales": forms.Textarea(attrs={
                "placeholder": "Ej.: Diabetes tipo 2, hipertensión, asma, etc.",
                "id": "id_antecedentes_personales",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "antecedentes_quirurgicos": forms.Textarea(attrs={
                "placeholder": "Ej.: Cirugías previas como apendicectomía, cesárea, etc.",
                "id": "id_antecedentes_quirurgicos",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "antecedentes_familiares": forms.Textarea(attrs={
                "placeholder": "Enfermedades hereditarias (padres, abuelos, hermanos).",
                "id": "id_antecedentes_familiares",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "alergias": forms.Textarea(attrs={
                "placeholder": "Ej.: Penicilina, mariscos, polvo, etc.",
                "id": "id_alergias",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "medicamentos_actuales": forms.Textarea(attrs={
                "placeholder": "Nombre, dosis y frecuencia. Ej.: Losartán 50mg diario.",
                "id": "id_medicamentos_actuales",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "habitos_toxicos": forms.TextInput(attrs={
                "placeholder": "Ej.: Tabaco, alcohol, drogas, sedentarismo, etc.",
                "id": "id_habitos_toxicos",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "vacunas": forms.Textarea(attrs={
                "placeholder": "Vacunas importantes recibidas. Ej.: COVID-19, influenza, etc.",
                "id": "id_vacunas",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
            }),
            "antecedentes_gineco_obstetricos": forms.Textarea(attrs={
                "placeholder": "Solo en mujeres. Ej.: menarquia, embarazos, anticonceptivos.",
                "id": "id_antecedentes_gineco_obstetricos",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                "rows": 3,
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
            "telefono": "Teléfono(s)",
            "email": "Correo Electrónico",
            "sexo": "Sexo",
            "estado_civil": "Estado Civil",
            "direccion": "Dirección Domiciliaria",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "tipo_sangre": "Tipo de Sangre",
            "foto": "Foto del Paciente",
            "antecedentes_personales": "Antecedentes Personales",
            "antecedentes_quirurgicos": "Antecedentes Quirúrgicos",
            "antecedentes_familiares": "Antecedentes Familiares",
            "alergias": "Alergias",
            "medicamentos_actuales": "Medicamentos Actuales",
            "habitos_toxicos": "Hábitos Tóxicos",
            "vacunas": "Vacunas",
            "antecedentes_gineco_obstetricos": "Antecedentes Gineco-Obstétricos",
            "activo": "Activo"
        }

    @property
    def id(self):
        return self.instance.pk if self.instance else None

    