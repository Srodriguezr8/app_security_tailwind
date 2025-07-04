
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View

from applications.core.form.foto_paciente import FotoPacienteForm
from applications.core.models import  FotoPaciente
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.module import ModuleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class FotoPacienteListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/fotos_paciente/list.html'
    model = FotoPaciente
    context_object_name = 'fotos_paciente'
    permission_required = 'view_fotopaciente'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(paciente__cedula_ecuatoriana__icontains=q1), Q.OR)
            self.query.add(Q(paciente__dni__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
            self.query.add(Q(fecha_subida__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:foto_paciente_create')

        return context


class FotoPacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = FotoPaciente
    template_name = 'core/fotos_paciente/form.html'
    form_class = FotoPacienteForm
    success_url = reverse_lazy('core:foto_paciente_list')
    permission_required = 'add_fotopaciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Foto del Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        foto_paciente = self.object
        messages.success(self.request, f"Éxito al crear la foto del paciente {foto_paciente.paciente.nombres} {foto_paciente.paciente.apellidos}.")
        return response


class FotoPacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = FotoPaciente
    template_name = 'core/fotos_paciente/form.html'
    form_class = FotoPacienteForm
    success_url = reverse_lazy('core:foto_paciente_list')
    permission_required = 'change_fotopaciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Foto del Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        foto_paciente = self.object
        messages.success(self.request, f"Éxito al actualizar la foto del paciente {foto_paciente.paciente.nombres} {foto_paciente.paciente.apellidos}.")
        return response


class FotoPacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = FotoPaciente
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:foto_paciente_list')
    permission_required = 'delete_fotopaciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar foto del paciente'
        foto_paciente = self.object
        context['description'] = f"¿Desea eliminar la foto del paciente: {foto_paciente.paciente.nombres} {foto_paciente.paciente.apellidos}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        foto_paciente = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente la foto del paciente: {foto_paciente.paciente.nombres} {foto_paciente.paciente.apellidos}.")
        
        return response
    
