
import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from applications.core.form.medicamento import MedicamentoForm
from applications.core.models import  MarcaMedicamento, Medicamento, TipoMedicamento
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/medicamentos/list.html'
    model = Medicamento
    context_object_name = 'medicamentos'
    permission_required = 'view_medicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(tipo__nombre__icontains=q1), Q.OR)
            self.query.add(Q(marca__nombre__icontains=q1), Q.OR)
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
            self.query.add(Q(concentracion__icontains=q1), Q.OR)
            self.query.add(Q(via_administracion__icontains=q1), Q.OR)
            self.query.add(Q(cantidad__icontains=q1), Q.OR)
            self.query.add(Q(precio__icontains=q1), Q.OR)
            self.query.add(Q(comercial__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')

        return context


class MedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    template_name = 'core/medicamentos/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'add_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        messages.success(self.request, f"Éxito al crear el medicamento {medicamento.nombre}.")
        return response


class MedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    template_name = 'core/medicamentos/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'change_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        messages.success(self.request, f"Éxito al actualizar el medicamento {medicamento.nombre}.")
        return response


class MedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'delete_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar medicamento'
        medicamento = self.object
        context['description'] = f"¿Desea eliminar el medicamento: {medicamento.nombre}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        medicamento = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el medicamento: {medicamento.nombre}.")
        
        return response
    
class SaveMedicamentoView(View):
    def post(self,request,*args,**kargs):
        try:
            form = MedicamentoForm(request.POST, request.FILES)
            id = request.POST.get('medicamento_id')
            medicamento = Medicamento.objects.get(pk=id)
            form = MedicamentoForm(request.POST, request.FILES, instance=medicamento)
            if form.is_valid():
                medicamento = form.save(commit=False)
            
                borrar_imagen = request.POST.get('borrar_imagen') == 'true'

                if borrar_imagen and medicamento.foto:
                    medicamento.foto.delete(save=False)
                    medicamento.foto = None

                medicamento.save()

                return JsonResponse({'ok': True, 'medicamento': medicamento.nombre})
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

        except Exception as e:
            print('error al guardar')
            return JsonResponse({'ok': False, 'errors': str(e)}, status=400)
    

def crear_medicamento_ajax(request):
    try:

       
        tipo_id = request.POST.get('tipo')

        try:
            print(tipo_id)
        except Exception as e:
            print('e:', e)
        
        nombre = request.POST.get('nombre')
        via_administracion = request.POST.get('via_administracion')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')

        print('antes')
        print(tipo_id)
        tipo = TipoMedicamento.objects.get(pk=int(tipo_id))
        
        marca_id = request.POST.get('marca_medicamento')
        marca = None
        print('FILES:', request.FILES)
       

        print('pasa')
        if marca_id:
            try:
                marca = MarcaMedicamento.objects.get(pk=int(marca_id))
            except MarcaMedicamento.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Marca no válida'}, status=400)

        medicamento = Medicamento.objects.create(
            tipo=tipo,
            marca_medicamento=marca,
            nombre=nombre,
            descripcion=request.POST.get('descripcion'),
            concentracion=request.POST.get('concentracion'),
            via_administracion=via_administracion,
            cantidad=int(cantidad),
            precio=float(precio),
            comercial=request.POST.get('comercial') == 'on' if True else False,
            foto = request.FILES.get('foto') or None,
            activo=request.POST.get('activo') == 'on'  if True else False,
            
        )

        return JsonResponse({
            'success': True,
            'mensaje': 'Medicamento creado exitosamente',
            'id': medicamento.id,
            'nombre': medicamento.nombre
        })

    except TipoMedicamento.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tipo de medicamento no válido'}, status=400)
    except ValueError as e:
        return JsonResponse({'success': False, 'error': f'Error de valor: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
