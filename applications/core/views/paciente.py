import json
from django.forms import ValidationError
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from applications.core.form.paciente import PacienteForm
from applications.core.models import Paciente, TipoSangre


from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from applications.core.form.medicamento import MedicamentoForm
from applications.core.models import  Medicamento
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/pacientes/list.html'
    model = Paciente
    context_object_name = 'pacientes'
    permission_required = 'view_paciente'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombres__icontains=q1), Q.OR)
            self.query.add(Q(apellidos__icontains=q1), Q.OR)
            self.query.add(Q(cedula_ecuatoriana__icontains=q1), Q.OR)
            self.query.add(Q(dni__icontains=q1), Q.OR)
            self.query.add(Q(fecha_nacimiento__icontains=q1), Q.OR)
            self.query.add(Q(telefono__icontains=q1), Q.OR)
            self.query.add(Q(email__icontains=q1), Q.OR)
            self.query.add(Q(sexo__icontains=q1), Q.OR)
            self.query.add(Q(estado_civil__icontains=q1), Q.OR)
            self.query.add(Q(direccion__icontains=q1), Q.OR)
            self.query.add(Q(tipo_sangre__tipo__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:paciente_create')

        return context


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Paciente'
        context['back_url'] = self.success_url
        
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        paciente = self.object
        messages.success(self.request, f"Éxito al crear el paciente {paciente.nombres.split()[0]} {paciente.apellidos.split()[0]}.")
        return response


class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        paciente = self.object
        messages.success(self.request, f"Éxito al actualizar el paciente {paciente.nombres.split()[0]} {paciente.apellidos.split()[0]}.")
        return response


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar paciente'
        paciente = self.object
        context['description'] = f"¿Desea eliminar el paciente: {paciente.nombres.split()[0]} {paciente.apellidos.split()[0]}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        paciente = self.object
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el paciente: {paciente.nombres.split()[0]} {paciente.apellidos.split()[0]}.")
        
        return response
    

class SavePacienteView(View):
    def post(self,request,*args,**kargs):
        try:
            form = PacienteForm(request.POST, request.FILES)
            id = request.POST.get('paciente_id')
            paciente = Paciente.objects.get(pk=id)
            form = PacienteForm(request.POST, request.FILES, instance=paciente)
            if form.is_valid():
                paciente = form.save(commit=False)
            
                borrar_imagen = request.POST.get('borrar_imagen') == 'true'

                if borrar_imagen and paciente.foto:
                    paciente.foto.delete(save=False)
                    paciente.foto = None

                paciente.save()

                return JsonResponse({'ok': True, 
                                     'paciente': f"{paciente.nombres.split()[0]} {paciente.apellidos.split()[0]}"
                                     })
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

        except Exception as e:
            print('error al guardar')
            return JsonResponse({'ok': False, 'errors': str(e)}, status=400)
    

def crear_paciente_ajax(request):
    try:
        data = json.loads(request.body)

        paciente = Paciente(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            cedula_ecuatoriana=data.get('cedula_ecuatoriana'),
            dni=data.get('dni'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            telefono=data.get('telefono'),
            email=data.get('email') or None,
            sexo=data.get('sexo'),
            estado_civil=data.get('estado_civil'),
            direccion=data.get('direccion'),
            latitud=data.get('latitud') or None,
            longitud=data.get('longitud') or None,
            tipo_sangre=TipoSangre.objects.get(pk=data['tipo_sangre']) if data.get('tipo_sangre') else None,
            antecedentes_personales=data.get('antecedentes_personales'),
            antecedentes_quirurgicos=data.get('antecedentes_quirurgicos'),
            antecedentes_familiares=data.get('antecedentes_familiares'),
            alergias=data.get('alergias'),
            medicamentos_actuales=data.get('medicamentos_actuales'),
            habitos_toxicos=data.get('habitos_toxicos', 'ninguno'),
            vacunas=data.get('vacunas'),
            antecedentes_gineco_obstetricos=data.get('antecedentes_gineco_obstetricos'),
            activo=data.get('activo')=='on'if True else False
        )
        paciente.save()
        print(paciente.activo)

        return JsonResponse({'success': True, 'id': paciente.id},status=200)

    except TipoSangre.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tipo de sangre inválido'}, status=400)

    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.message_dict}, status=400)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


"""  Vista para buscar pacientes mediante AJAX. Por nombres, apellidos, cédula o teléfono. """
@login_required
@require_http_methods(["GET"])
def paciente_find(request):
    try:
        # Obtener el parámetro de búsqueda
        query = request.GET.get('q', '').strip()

        # Validar que se proporcione al menos 3 caracteres
        if len(query) < 3:
            return JsonResponse({
                'success': False,
                'message': 'Debe proporcionar al menos 3 caracteres para la búsqueda',
                'pacientes': []
            })

        # Construir la consulta de búsqueda
        # Buscar en nombres, apellidos, cédula, DNI y teléfono
        pacientes_query = Paciente.objects.filter(
            Q(activo=True) & (
                    Q(nombres__icontains=query) |
                    Q(apellidos__icontains=query) |
                    Q(cedula_ecuatoriana__icontains=query) |
                    Q(dni__icontains=query) |
                    Q(telefono__icontains=query)
            )
        ).select_related('tipo_sangre').prefetch_related(
            'atenciones__diagnostico',
            'atenciones__detalles__medicamento'
        ).order_by('apellidos', 'nombres')

        # Limitar resultados para mejorar rendimiento
        pacientes_query = pacientes_query[:20]

        # Convertir a lista de diccionarios
        pacientes_data = []
        for paciente in pacientes_query:
            # Calcular edad
            edad = paciente.edad

            # Obtener atenciones anteriores (últimas 10)
            atenciones = []
            for atencion in paciente.atenciones.all()[:10]:
                # Obtener prescripciones/detalles de esta atención
                detalles = []
                for detalle in atencion.detalles.all():
                    detalle_dict = {
                        'medicamento': detalle.medicamento.nombre if detalle.medicamento else None,
                        'cantidad': detalle.cantidad,
                        'prescripcion': detalle.prescripcion,
                        'duracion_tratamiento': detalle.duracion_tratamiento,
                        'frecuencia_diaria': detalle.frecuencia_diaria,
                    }
                    detalles.append(detalle_dict)

                # Obtener diagnósticos
                diagnosticos = [d.descripcion for d in atencion.diagnostico.all()]

                # Determinar tipo de consulta
                tipo_consulta = "Chequeo"
                if atencion.es_control:
                    tipo_consulta = "Control"
                elif "urgencia" in atencion.motivo_consulta.lower() or "dolor" in atencion.motivo_consulta.lower():
                    tipo_consulta = "Urgencia"

                atencion_dict = {
                    'id': atencion.id,
                    'fecha_atencion': atencion.fecha_atencion.isoformat(),
                    'tipo_consulta': tipo_consulta,

                    # Signos vitales
                    'presion_arterial': atencion.presion_arterial,
                    'pulso': atencion.pulso,
                    'temperatura': float(atencion.temperatura) if atencion.temperatura else None,
                    'frecuencia_respiratoria': atencion.frecuencia_respiratoria,
                    'saturacion_oxigeno': float(atencion.saturacion_oxigeno) if atencion.saturacion_oxigeno else None,
                    'peso': float(atencion.peso) if atencion.peso else None,
                    'altura': float(atencion.altura) if atencion.altura else None,
                    'imc': atencion.calcular_imc,

                    # Contenido de la atención
                    'motivo_consulta': atencion.motivo_consulta,
                    'sintomas': atencion.sintomas,
                    'tratamiento': atencion.tratamiento,
                    'diagnosticos': diagnosticos,
                    'examen_fisico': atencion.examen_fisico,
                    'examenes_enviados': atencion.examenes_enviados,
                    'comentario_adicional': atencion.comentario_adicional,
                    'es_control': atencion.es_control,

                    # Prescripciones
                    'prescripciones': detalles
                }
                atenciones.append(atencion_dict)

            paciente_dict = {
                'id': paciente.id,
                'nombres': paciente.nombres,
                'apellidos': paciente.apellidos,
                'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
                'dni': paciente.dni,
                'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                'edad': edad,
                'telefono': paciente.telefono,
                'email': paciente.email,
                'sexo': paciente.sexo,
                'estado_civil': paciente.estado_civil,
                'direccion': paciente.direccion,
                'latitud': float(paciente.latitud) if paciente.latitud else None,
                'longitud': float(paciente.longitud) if paciente.longitud else None,
                'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
                'foto_url': paciente.get_image,

                # Historia clínica
                'antecedentes_personales': paciente.antecedentes_personales,
                'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
                'antecedentes_familiares': paciente.antecedentes_familiares,
                'alergias': paciente.alergias,
                'medicamentos_actuales': paciente.medicamentos_actuales,
                'habitos_toxicos': paciente.habitos_toxicos,
                'vacunas': paciente.vacunas,
                'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,

                # Atenciones anteriores
                'atenciones': atenciones,
                'total_atenciones': paciente.atenciones.count()
            }
            pacientes_data.append(paciente_dict)
        print(pacientes_data)
        return JsonResponse({
            'success': True,
            'pacientes': pacientes_data,
            'total': len(pacientes_data),
            'query': query
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error en la búsqueda: {str(e)}',
            'pacientes': []
        }, status=500)


