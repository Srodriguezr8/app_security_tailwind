from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from applications.core.models import Paciente
from applications.doctor.models import CitaMedica
from applications.security.components.mixin_crud import SessionGroupMixin,  PermissionMixin, ListViewMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json


class AgendaCitaMedicaListView(SessionGroupMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/citas/agendar_cita.html'
    model = CitaMedica
    context_object_name = 'citas'
    permission_required = 'view_citas'

    def get_queryset(self):
        q1 = self.request.GET.get('q')

        if q1  is not None:
               self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
               self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
               self.query.add(Q(motivo_consulta__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('-fecha')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_create')

        return context
    

@login_required
def add_patient_api(request):
    print('llego a api')
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        patientData = json.loads(request.body)
        
        if not patientData:
            return JsonResponse({
                'success': False,
                'message': 'No se obtuvo los datos del paciente',
                'data': None
            })
        # validated email 
        email = patientData.get('email')
        if Paciente.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': f'El existe un paciente con el correo {email}',
                'data': None
            }, status=409)
            
        # validated cedula
        cedula_ecuatoriana = patientData.get('cedula_ecuatoriana')
        if Paciente.objects.filter(cedula_ecuatoriana=cedula_ecuatoriana).exists():
            return JsonResponse({
                'success': False,
                'message': f'Ya existe un paciente con la cedula {cedula_ecuatoriana}',
                'data': None
            }, status=409)

        newPatient = Paciente.objects.create(
                nombres=patientData.get('nombres'),
                apellidos=patientData.get('apellidos'),
                cedula_ecuatoriana=patientData.get('cedula_ecuatoriana'),
                fecha_nacimiento=patientData.get('fecha_nacimiento'),
                email=patientData.get('email'),
                telefono=patientData.get('telefono'),
                estado_civil=patientData.get('estado_civil'),
                direccion=patientData.get('direccion'),
                antecedentes_personales=patientData.get('antecedentes_personales'),
                alergias=patientData.get('alergias'),
                medicamentos_actuales=patientData.get('medicamentos_actuales')
            )

        return JsonResponse({
            'success': True,
            'message': 'Paciente registrado correctamente',
            'data':  {'id': newPatient.id}
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except IntegrityError as e:
        print(f"[ERROR] Error en add_patient_api: {e}")
    except Exception as e:
        print(f"[ERROR] Error en add_patient_api: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    