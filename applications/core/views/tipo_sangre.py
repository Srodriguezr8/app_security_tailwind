
from django.contrib import messages
from django.urls import reverse_lazy

from applications.core.form.tipo_sangre import TipoSangreForm
from applications.core.models import  TipoSangre
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class TipoSangreListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipo_sangres/list.html'
    model = TipoSangre
    context_object_name = 'tipo_sangres'
    permission_required = 'view_tiposangre'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(tipo__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_sangre_create')

        return context


class TipoSangreCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tipo_sangres/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'add_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        messages.success(self.request, f"Éxito al crear el tipo de sangre {tipo_sangre.tipo}.")
        return response


class TipoSangreUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoSangre
    template_name = 'core/tipo_sangres/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'change_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        messages.success(self.request, f"Éxito al actualizar el tipo de sangre {tipo_sangre.tipo}.")
        return response


class TipoSangreDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoSangre
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:tipo_sangre_list')
    permission_required = 'delete_tiposangre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar tipo de gesto'
        tipo_sangre = self.object
        context['description'] = f"¿Desea eliminar el tipo de sangre: {tipo_sangre.tipo}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        tipo_sangre = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el tipo de sangre: {tipo_sangre.tipo}.")
        
        return response