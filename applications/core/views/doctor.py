
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from applications.core.form.doctor import DoctorForm
from applications.core.models import Doctor
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.db.models import Q


class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/doctores/list.html'
    model = Doctor
    context_object_name = 'doctores'
    permission_required = 'view_doctor'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(codigo__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
            self.query.add(Q(datos_adicionales__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:doctor_create')

        return context


class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    template_name = 'core/doctores/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        messages.success(self.request, f"Éxito al crear el doctor {doctor.nombres}.")
        return response


class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    template_name = 'core/doctores/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        
        messages.success(self.request, f"Éxito al actualizar el doctor {doctor.nombres.split()[0]} {doctor.apellidos.split()[0]}.")
        return response


class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar el doctor: {self.nombres.split()[0]} {self.apellidos.split()[0]}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        doctor = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el doctor {doctor.nombres.split()[0]} {doctor.apellidos.split()[0]}.")
        
        return response
    


class EspecialidadDoctorView(DetailView):
    model=Doctor
    def get(self,request, *args,**kargs):
        try:
            obj = self.get_object()

            especialidades = list(obj.especialidad.all())
            especialidades = [d.nombre for d in especialidades]

            return JsonResponse({
                'especialidades':especialidades,
                'message':'OK'
                })
        
        except Exception as e:
            return JsonResponse({
                'especialidades':[],
                'message': f"Error: {str(e)}"
            },status = 404)

        