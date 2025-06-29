
import json
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone

from applications.core.models import Paciente, Medicamento, Diagnostico
from applications.doctor.forms.atencion import AtencionForm
from applications.doctor.models import Atencion, CitaMedica, DetalleAtencion
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, \
    PermissionMixin, SessionGroupMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class AgendaCitaMedicaListView(SessionGroupMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/citas/agendar_cita.html'
    model = CitaMedica
    context_object_name = 'citas'
    permission_required = 'view_citas'

    def get_queryset(self):
        q1 = self.request.GET.get('q')

        if q1  is not None:
               self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
               self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
               self.query.add(Q(motivo_consulta__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('-fecha')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_create')

        return context
    
