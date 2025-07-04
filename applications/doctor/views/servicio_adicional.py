
from django.contrib import messages
from django.urls import reverse_lazy


from applications.doctor.forms.servicio_adicional import ServicioAdicionalForm
from applications.doctor.models import ServiciosAdicionales
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class ServicioAdicionalListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/servicios_adicionales/list.html'
    model = ServiciosAdicionales
    context_object_name = 'servicios_adicionales'
    permission_required = 'view_serviciosadicionales'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre_servicio__icontains=q1), Q.OR)
            self.query.add(Q(costo_servicio__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:servicio_adicional_create')

        return context


class ServicioAdicionalCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/form.html'
    form_class = ServicioAdicionalForm
    success_url = reverse_lazy('doctor:servicio_adicional_list')
    permission_required = 'add_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Servicio Adicional'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        servicio = self.object
        messages.success(self.request, f"Éxito al crear el servicio {servicio.nombre_servicio}.")
        return response


class ServicioAdicionaloUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/form.html'
    form_class = ServicioAdicionalForm
    success_url = reverse_lazy('doctor:servicio_adicional_list')
    permission_required = 'change_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Servicio Adicional'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        servicio = self.object
        messages.success(self.request, f"Éxito al actualizar el servicio {servicio.nombre_servicio}.")
        return response


class ServicioAdicionalDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:servicio_adicional_list')
    permission_required = 'delete_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Servicio Adicional'
        servicio = self.object
        context['description'] = f"¿Desea eliminar elservicio: {servicio.nombre_servicio}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        servicio = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el servicio: {servicio.nombre_servicio}.")
        
        return response