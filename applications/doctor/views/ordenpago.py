from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from applications.doctor.forms.ordenpago import PagoForm, DetallePagoFormSet, DetallePago, DetallePagoForm
from applications.doctor.models import Pago, OrdenPago, ServiciosAdicionales
from applications.security.components.mixin_crud import PermissionMixin
from django.http import JsonResponse
from applications.doctor.models import Pago
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.utils import timezone

class OrdenPagoCreateView(LoginRequiredMixin, PermissionMixin, CreateView):
    model = Pago
    template_name = 'core/pagos/form.html'
    form_class = PagoForm
    #success_url = reverse_lazy('doctor:pagos_list')  # Cambia por tu url real
    permission_required = 'add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DetallePagoFormSet(self.request.POST, queryset=DetallePago.objects.none())
        else:
            context['formset'] = DetallePagoFormSet(queryset=DetallePago.objects.none())
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
            #messages.success(self.request, "Registrado correctamente.")

            # --- AJAX (no cambies esta parte) ---
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"ok": True, "pago_id": self.object.id})

            # --- REDIRECT limpio en caso normal ---
            return HttpResponseRedirect(self.request.path)

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

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
import json

@csrf_exempt
@require_http_methods(["POST"])
def crear_servicio_adicional(request):
    """
    API para crear un nuevo servicio adicional
    """
    try:
        # Validar Content-Type
        if request.content_type != 'application/json':
            return JsonResponse({"error": "Content-Type debe ser application/json"}, status=400)
        
        # Parsear JSON
        if not request.body:
            return JsonResponse({"error": "No se enviaron datos."}, status=400)
            
        data = json.loads(request.body.decode("utf-8"))
        
        # Validar campos
        nombre = data.get("nombre_servicio", "").strip()
        costo = data.get("costo_servicio")
        descripcion = data.get("descripcion", "").strip()
        
        if not nombre:
            return JsonResponse({"error": "El nombre del servicio es obligatorio."}, status=400)
        
        if not costo:
            return JsonResponse({"error": "El costo del servicio es obligatorio."}, status=400)
        
        # Validar y convertir costo
        try:
            costo_decimal = float(costo)
            if costo_decimal <= 0:
                return JsonResponse({"error": "El costo debe ser mayor a 0."}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({"error": "El costo debe ser un número válido."}, status=400)
        
        # Crear servicio
        servicio = ServiciosAdicionales.objects.create(
            nombre_servicio=nombre,
            costo_servicio=costo_decimal,
            descripcion=descripcion,
            activo=True
        )
        
        # Respuesta exitosa
        response_data = {
            "id": servicio.id,
            "nombre_servicio": servicio.nombre_servicio,
            "costo_servicio": float(servicio.costo_servicio),
            "descripcion": servicio.descripcion
        }
        
        return JsonResponse(response_data, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Datos JSON inválidos."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error interno del servidor: {str(e)}"}, status=500)

#valor consulta
def get_valor_consulta(request, pago_id):
    try:
        pago = Pago.objects.get(pk=pago_id)
        return JsonResponse({'valor_consulta': float(pago.monto_total)})
    except Pago.DoesNotExist:
        return JsonResponse({'error': 'No existe ese Pago'}, status=404)
    
# --- NUEVO API para obtener el costo de un servicio adicional ---

def get_costo_servicio_adicional(request, servicio_id):
    try:
        servicio = ServiciosAdicionales.objects.get(pk=servicio_id)
        return JsonResponse({'costo_servicio': float(servicio.costo_servicio)})
    except ServiciosAdicionales.DoesNotExist:
        return JsonResponse({'error': 'No existe ese Servicio'}, status=404)
    
## Endpoint para guardar un detalle

from django.views.decorators.http import require_POST

from decimal import Decimal, InvalidOperation

def safe_decimal(val):
    try:
        return Decimal(str(val)) if str(val).strip() not in ["", None] else Decimal(0)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(0)

@require_POST
def guardar_detalle_pago(request):
    data = json.loads(request.body.decode('utf-8'))
    print('DEBUG data recibida:', data)
    try:
        from applications.doctor.models import DetallePago, Pago, ServiciosAdicionales
        pago = Pago.objects.get(pk=data['pago'])
        servicio = ServiciosAdicionales.objects.get(pk=data['servicio_adicional'])
        detalle = DetallePago.objects.create(
            pago=pago,
            servicio_adicional=servicio,
            cantidad=int(data.get('cantidad', 1) or 1),
            precio_unitario=safe_decimal(data.get('precio_unitario', 0)),
            valor_consulta=safe_decimal(data.get('valor_consulta', 0)),
            descuento_porcentaje=safe_decimal(data.get('descuento_porcentaje', 0)),
            aplica_seguro=bool(data.get('aplica_seguro', False)),
            valor_seguro=safe_decimal(data.get('valor_seguro', 0)),
            descripcion_seguro=data.get('descripcion_seguro', ''),
        )
        return JsonResponse({'ok': True, 'id': detalle.id})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})
#AJAX PARA DETALLE DE PAGO
from django.shortcuts import render, get_object_or_404

def detalles_pago_tbody_ajax(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    detalles = pago.detalles.all()
    html = render(request, "core/pago/partials/detalles_pago_tbody.html", {"detalles": detalles}).content.decode("utf-8")
    return JsonResponse({"html": html})