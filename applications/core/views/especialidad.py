
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.especialidad import EspecialidadForm
from applications.core.models import  Especialidad
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.module import ModuleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class EspecialidadListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/especialidades/list.html'
    model = Especialidad
    context_object_name = 'especialidades'
    permission_required = 'view_especialidad'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:especialidad_create')

        return context


class EspecialidadCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Especialidad
    template_name = 'core/especialidades/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'add_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        messages.success(self.request, f"Éxito al crear la especialidad {especialidad.nombre}.")
        return response


class EspecialidadUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Especialidad
    template_name = 'core/especialidades/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'change_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        messages.success(self.request, f"Éxito al actualizar la especialidad {especialidad.nombre}.")
        return response


class EspecialidadDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Especialidad
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:especialidad_list')
    permission_required = 'delete_especialidad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar especialidad'
        especialidad = self.object
        context['description'] = f"¿Desea eliminar la especialidad: {especialidad.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        especialidad = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente la especialidad: {especialidad.nombre}.")
        
        return response