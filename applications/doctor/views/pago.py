from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.doctor.models import Pago

class PagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = "core/pagos/list.html"
    context_object_name = "pagos"
    queryset = Pago.objects.filter(activo=True)

class PagoCreateView(LoginRequiredMixin, CreateView):
    model = Pago
    fields = [
        "atencion", "metodo_pago", "monto_total", "estado", "fecha_pago",
        "nombre_pagador", "referencia_externa", "evidencia_pago", "observaciones", "activo"
    ]
    template_name = "core/pago/form.html"
    success_url = reverse_lazy("doctor:pago_list")

class PagoUpdateView(LoginRequiredMixin, UpdateView):
    model = Pago
    fields = [
        "atencion", "metodo_pago", "monto_total", "estado", "fecha_pago",
        "nombre_pagador", "referencia_externa", "evidencia_pago", "observaciones", "activo"
    ]
    template_name = "doctor/pago_form.html"
    success_url = reverse_lazy("doctor:pago_list")

class PagoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = "doctor/pago_confirm_delete.html"
    success_url = reverse_lazy("doctor:pago_list")
