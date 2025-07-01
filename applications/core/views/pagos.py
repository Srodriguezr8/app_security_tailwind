# core/views.py

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404, redirect
from applications.core.models import PagoPendiente
from django.urls import reverse
from django.http import JsonResponse

class PagosPendientesListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = PagoPendiente
    template_name = 'core/pagos/list.html'
    context_object_name = 'pagos'
    permission_required = 'view__pagos'

    def get_queryset(self):
        return PagoPendiente.objects.filter(usuario=self.request.user, pagado=False)

# La vista para marcar el pago como realizado
class RealizarPagoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        pago = get_object_or_404(PagoPendiente, pk=pk, usuario=request.user, pagado=False)
        # Aquí deberías integrar la verificación real con PayPal
        pago.pagado = True
        pago.save()
        return JsonResponse({'ok': True})
