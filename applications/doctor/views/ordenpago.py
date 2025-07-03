from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from applications.doctor.forms.ordenpago import PagoForm, DetallePagoFormSet, DetallePago, DetallePagoForm
from applications.doctor.models import Pago, OrdenPago, ServiciosAdicionales
from applications.security.components.mixin_crud import PermissionMixin
from django.http import JsonResponse
from applications.doctor.models import Pago

class OrdenPagoCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Pago
    template_name = 'core/pago/form.html'
    form_class = PagoForm
    #success_url = reverse_lazy('doctor:pagos_list')  # Cambia por tu url real
    permission_required = 'add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DetallePagoFormSet(self.request.POST)
        else:
            context['formset'] = DetallePagoFormSet()
        context['title'] = "Registrar Pago"
        context['title1'] = "REGISTRO DE PAGO"
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        metodo_pago = self.request.POST.get('metodo_pago')
        referencia = self.request.POST.get('referencia_externa')
        if formset.is_valid():
            self.object = form.save(commit=False)
            if metodo_pago:
                self.object.metodo_pago = metodo_pago
            if referencia:
                self.object.referencia_externa = referencia
            self.object.save()
            formset.instance = self.object
            formset.save()
            orden = OrdenPago(self.object)
            if self.object.detalles.exists():
                orden.actualizar_total()
            self.object.refresh_from_db()
            # Para mostrar el mensaje una sola vez
            messages.success(self.request, "Registrado correctamente.")
            # Devuelve el formulario con los datos escritos
            return self.render_to_response(self.get_context_data(form=form, formset=formset, just_registered=True))
        else:
            messages.error(self.request, "Hay errores en el formulario o los detalles.")
            return self.render_to_response(self.get_context_data(form=form))


from django.forms import modelformset_factory

DetallePagoFormSet = modelformset_factory(
    DetallePago,
    form=DetallePagoForm,
    extra=3,
    can_delete=True,
)

## API PARA SERVICIOS ADICIONALES ##
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
import json

#@csrf_exempt
def crear_servicio_adicional(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        nombre = data.get("nombre_servicio")
        costo = data.get("costo_servicio")
        descripcion = data.get("descripcion")
        if not (nombre and costo):
            return JsonResponse({"error": "Faltan campos obligatorios."}, status=400)
        serv = ServiciosAdicionales.objects.create(
            nombre_servicio=nombre,
            costo_servicio=costo,
            descripcion=descripcion or "",
            activo=True
        )
        return JsonResponse({"id": serv.id, "nombre_servicio": serv.nombre_servicio})
    return JsonResponse({"error": "Solo POST permitido"}, status=405)

#valor consulta
def get_valor_consulta(request, pago_id):
    try:
        pago = Pago.objects.get(pk=pago_id)
        return JsonResponse({'valor_consulta': float(pago.monto_total)})
    except Pago.DoesNotExist:
        return JsonResponse({'error': 'No existe ese Pago'}, status=404)