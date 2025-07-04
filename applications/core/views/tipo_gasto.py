
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.tipo_gasto import TipoGastoForm
from applications.core.models import  TipoGasto
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class TipoGastoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipo_gastos/list.html'
    model = TipoGasto
    context_object_name = 'tipo_gastos'
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_gasto_create')

        return context


class TipoGastoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    template_name = 'core/tipo_gastos/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'add_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo Gasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_gasto = self.object
        messages.success(self.request, f"Éxito al crear el tipo de gasto {tipo_gasto.nombre}.")
        return response


class TipoGastoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    template_name = 'core/tipo_gastos/form.html'
    form_class = TipoGastoForm
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'change_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo Gasto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_gasto = self.object
        messages.success(self.request, f"Éxito al actualizar el tipo de gasto {tipo_gasto.nombre}.")
        return response


class TipoGastoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'delete_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar tipo de gesto'
        tipo_gasto = self.object
        context['description'] = f"¿Desea eliminar el tipo de gasto: {tipo_gasto.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        tipo_gasto = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el tipo de gasto: {tipo_gasto.nombre}.")
        
        return response