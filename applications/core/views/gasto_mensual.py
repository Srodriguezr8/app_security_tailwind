
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.gasto_mensual import GastoMensualForm
from applications.core.models import  GastoMensual
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class GastoMensualListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/gastos_mensuales/list.html'
    model = GastoMensual
    context_object_name = 'gastos_mensuales'
    permission_required = 'view_gasto_mensual'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(tipo_gasto__nombre__icontains=q1), Q.OR)
            self.query.add(Q(fecha__icontains=q1), Q.OR)
            self.query.add(Q(valor__icontains=q1), Q.OR)
            self.query.add(Q(observacion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:gasto_mensual_create')

        return context


class GastoMensualCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    template_name = 'core/gastos_mensuales/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'add_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Gasto Mensual'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        gasto_mensual = self.object
        messages.success(self.request, f"Éxito al crear el gasto mensual {gasto_mensual.tipo_gasto.nombre}.")
        return response


class GastoMensualUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    template_name = 'core/gastos_mensuales/form.html'
    form_class = GastoMensualForm
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'change_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Gasto Mensual'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        gasto_mensual = self.object
        messages.success(self.request, f"Éxito al actualizar el gasto mensual {gasto_mensual.tipo_gasto.nombre}.")
        return response


class GastoMensualdDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'delete_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Gasto Mensual'
        gasto_mensual = self.object
        context['description'] = f"¿Desea eliminar el gasto mensual: {gasto_mensual.tipo_gasto.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        gasto_mensual = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el gasto mensual: {gasto_mensual.tipo_gasto.nombre}.")
        
        return response