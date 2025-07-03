
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.tipo_medicamento import TipoMedicamentoForm
from applications.core.models import  TipoMedicamento
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class TipoMedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipo_medicamentos/list.html'
    model = TipoMedicamento
    context_object_name = 'tipo_medicamentos'
    permission_required = 'view_tipomedicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_medicamento_create')

        return context


class TipoMedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamentos/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'add_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        messages.success(self.request, f"Éxito al crear el tipo de medicamento {tipo_medicamento.nombre}.")
        return response


class TipoMedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamentos/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'change_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        messages.success(self.request, f"Éxito al actualizar el tipo de medicamento {tipo_medicamento.nombre}.")
        return response


class TipoMedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:tipo_medicamento_list')
    permission_required = 'delete_tipomedicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar tipo de medicamentos'
        tipo_medicamento = self.object
        context['description'] = f"¿Desea eliminar el tipo de medicamento: {tipo_medicamento.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        tipo_medicamento = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el tipo de medicamento: {tipo_medicamento.nombre}.")
        
        return response