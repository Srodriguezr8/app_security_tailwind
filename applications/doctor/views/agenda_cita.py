import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from applications.core.models import Paciente
from applications.core.utils.paciente import CondicionMedicaChoices
from applications.doctor.models import CitaMedica
from applications.security.components.mixin_crud import SessionGroupMixin,  PermissionMixin, ListViewMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json
from django.db.models import Q

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
    
    
@login_required
def patients_search_api(request):
   
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    medical_conditions_labels = [choice[1] for choice in CondicionMedicaChoices.choices]
    
    try:
        search_text = request.GET.get('search', '').strip()
        limit = request.GET.get('limit', None) 
        order_by = request.GET.get('order_by', None)

        queryset = Paciente.objects.filter(Q(activo=True)) # Empezar con todos los pacientes

        # Aplicar filtro de búsqueda si hay un search_text
        if search_text:
            terms = [t for t in search_text.split() if t]
            if terms: # Solo aplica el filtro si hay términos válidos
                query_filters = Q()
                for term in terms:
                    query_filters |= Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(cedula_ecuatoriana__icontains=term)
                queryset = queryset.filter(query_filters)

        # Aplicar ordenación
        if order_by:
            valid_order_fields = ['id', 'nombres', 'apellidos', 'fecha_nacimiento', 'fecha_creacion', 'telefono'] # Agrega los campos válidos
            if order_by.startswith('-'):
                field = order_by[1:]
                if field in valid_order_fields:
                    queryset = queryset.order_by(order_by)
            elif order_by in valid_order_fields:
                queryset = queryset.order_by(order_by)
            else:
                print(f"Advertencia: Campo de ordenación '{order_by}' no válido o no seguro. Usando orden por defecto.")
                queryset = queryset.order_by('-id') # Fallback seguro
        else:
            # Ordenar por defecto por ID descendente (los últimos ingresados si ID es incremental)
            queryset = queryset.order_by('-id') 


        # Aplicar límite después de filtrar y ordenar
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit] 
            except ValueError:
                print(f"Advertencia: El límite '{limit}' no es un número válido. No se aplicará límite.")
        
        # Serializar los resultados
        data = []
        for p in queryset:
            random_condition_display = random.choice(medical_conditions_labels)
            data.append({
                'id': p.id,
                'nombres' : p.nombres,
                'apellidos': p.apellidos, 
                'fecha_nacimiento': p.fecha_nacimiento,
                'condition': random_condition_display,
                'priority': 'normal', 
                'phone': p.telefono,
            })
        

        return JsonResponse({
            'success': True,
            'message': 'Pacientes encontrados',
            'data': data
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except IntegrityError as e:
        print(f"[ERROR] Error en add_patient_api: {e}")
    except Exception as e:
        print(f"[ERROR] Error en add_patient_api: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    
       