from django import forms
from django.forms import ModelForm
from applications.security.models import GroupModulePermission

class GroupModulePermissionForm(ModelForm):
    class Meta:
        model = GroupModulePermission
        fields = [
            "group",
            "module",
            "permissions",  # plural, ManyToMany
        ]
        widgets = {
            "group": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 rounded-lg p-2.5 w-full",
            }),
            "module": forms.Select(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 rounded-lg p-2.5 w-full",
            }),
            "permissions": forms.CheckboxSelectMultiple(attrs={
                "class": "space-y-2",
            }),
        }
        labels = {
            "group": "Grupo",
            "module": "Módulo",
            "permissions": "Permisos",
        }
