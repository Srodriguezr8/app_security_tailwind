from django import forms
from django.forms import ModelForm
from applications.security.models import Group

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            "name",
            "permissions", 
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 rounded-lg p-2.5 w-full"
            }),
            "permissions": forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2",
            }),
        }
        labels = {
            "name": "Nombre",
            "permissions": "Permisos",
        }
