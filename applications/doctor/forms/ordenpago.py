from django import forms
from applications.doctor.models import Pago, DetallePago, ServiciosAdicionales

# Formulario base para la cabecera (Pago)
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion',
            'metodo_pago',
            'nombre_pagador',
            'observaciones',
            'estado',
            'fecha_pago',
            'referencia_externa',
            'evidencia_pago',
            'monto_total',
        ]

# Formulario para cada detalle (DetallePago)
class DetallePagoForm(forms.ModelForm):
    monto_pago = forms.DecimalField(
        label="Monto del Pago", 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'bg-gray-100'}))

    class Meta:
        model = DetallePago
        fields = [
            'pago',
            'servicio_adicional',
            'cantidad',
            'precio_unitario',
            'valor_consulta',           # <-- Agrega este campo nuevo
            'descuento_porcentaje',
            'aplica_seguro',
            'valor_seguro',
            'descripcion_seguro',
            # ... y cualquier otro campo
        ]
        widgets = {
            'valor_consulta': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio_adicional'].queryset = ServiciosAdicionales.objects.filter(activo=True)
        # Si ya tiene pago, carga el monto
        if self.instance and self.instance.pago_id:
            self.fields['monto_pago'].initial = self.instance.pago.monto_total

# Importante: ¡el Formset!
from django.forms import modelformset_factory

DetallePagoFormSet = modelformset_factory(
    DetallePago,
    form=DetallePagoForm,
    extra=3,    # Número de filas a mostrar por defecto
    can_delete=True, # Para permitir eliminar detalles en edición
)
