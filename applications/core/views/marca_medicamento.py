
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.marca_medicamento import MarcaMedicamentoForm
from applications.core.models import  MarcaMedicamento
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class MarcaMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/marca_medicamentos/list.html'
    model = MarcaMedicamento
    context_object_name = 'marca_medicamentos'
    permission_required = 'view_marcamedicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:marca_medicamento_create')

        return context


class MarcaMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamentos/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'add_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        marca_medicamento = self.object
        messages.success(self.request, f"Éxito al crear la marca de medicamento {marca_medicamento.nombre}.")
        return response


class MarcaMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamentos/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'change_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        marca_medicamento = self.object
        messages.success(self.request, f"Éxito al actualizar la marca de medicamento {marca_medicamento.nombre}.")
        return response


class MarcaMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:marca_medicamento_list')
    permission_required = 'delete_marcamedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar marca de medicamentos'
        marca_medicamento = self.object
        context['description'] = f"¿Desea eliminar la marca de medicamento: {marca_medicamento.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        marca_medicamento = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente la marca de medicamento: {marca_medicamento.nombre}.")
        
        return response