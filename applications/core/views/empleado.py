
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from applications.core.form.diagnosticco import DiagnosticoForm
from applications.core.form.empleado import EmpleadoForm
from applications.core.models import  Empleado
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.module import ModuleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class EmpleadoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/empleados/list.html'
    model = Empleado
    context_object_name = 'empleados'
    permission_required = 'view_empleado'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombres__icontains=q1), Q.OR)
            self.query.add(Q(apellidos__icontains=q1), Q.OR)
            self.query.add(Q(cedula_ecuatoriana__icontains=q1), Q.OR)
            self.query.add(Q(dni__icontains=q1), Q.OR)
            self.query.add(Q(cargo__nombre__icontains=q1), Q.OR)
            self.query.add(Q(sueldo__icontains=q1), Q.OR)
            self.query.add(Q(fecha_ingreso__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:empleado_create')

        return context


class EmpleadoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    template_name = 'core/empleados/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'add_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        messages.success(self.request, f"Éxito al crear el empleado {empleado.nombres.split()[0]} {empleado.apellidos.split()[0]}.")
        return response


class EmpleadoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    template_name = 'core/empleados/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'change_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        messages.success(self.request, f"Éxito al actualizar el empleado {empleado.nombres.split()[0]} {empleado.apellidos.split()[0]}.")
        return response


class EmpleadoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'delete_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Empleado'
        empleado = self.object
        context['description'] = f"¿Desea eliminar el empleado: {empleado.nombres.split()[0]} {empleado.apellidos.split()[0]}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        empleado = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el empleado {empleado.nombres.split()[0]} {empleado.apellidos.split()[0]}.")
        
        return response
    
class SaveEmpleadoView(View):
    def post(self,request,*args,**kargs):
        try:
            form = EmpleadoForm(request.POST, request.FILES)
            id = request.POST.get('empleado_id')
            empleado = Empleado.objects.get(pk=id)
            form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
            if form.is_valid():
                empleado = form.save(commit=False)
            
                borrar_imagen = request.POST.get('borrar_imagen') == 'true'

                if borrar_imagen and empleado.foto:
                    empleado.foto.delete(save=False)
                    empleado.foto = None

                empleado.save()

                return JsonResponse({'ok': True, 'empleado': empleado.nombres.split()[0]+' '+ empleado.apellidos.split()[0]})
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

        except Exception as e:

            return JsonResponse({'ok': False, 'errors': str(e)}, status=400)
    

