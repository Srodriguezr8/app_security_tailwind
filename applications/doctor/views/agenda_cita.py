from datetime import datetime, date
from http.client import PRECONDITION_FAILED
import random
import logging
from turtle import pencolor
from typing import Any, Dict, List, Tuple
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db import IntegrityError, transaction
from applications.core.models import Doctor, Especialidad, Paciente
from django.core.exceptions import ValidationError
from applications.core.utils.paciente import CondicionMedicaChoices, CondicionPacienteChoices, TipoCitaChoices
from applications.doctor.models import CitaMedica
from applications.doctor.utils.cita_medica import EstadoCitaChoices
from applications.security.components.mixin_crud import SessionGroupMixin,  PermissionMixin, ListViewMixin
from django.utils.dateparse import parse_date, parse_time
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json
from django.db.models import Q

logger = logging.getLogger(__name__)
# Constantes
REQUIRED_APPOINTMENT_FIELDS = ['paciente_id', 'medico_id', 'fecha', 'hora_cita', 'tipo_cita','especialidad_id']
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'

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
        priorities = ['normal', 'urgent', 'follow-up']
        data = []
        for p in queryset:
            random_condition_display = random.choice(medical_conditions_labels)
            priority = random.choice(priorities)
            data.append({
                'id': p.id,
                'nombres': p.nombres,
                'apellidos': p.apellidos,
                'fecha_nacimiento': p.fecha_nacimiento,
                'condition': random_condition_display,
                'priority': priority,
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
 


@csrf_exempt
@login_required
def appointments_api(request):
    """
    API para gestionar citas médicas (crear y eliminar).
    
    POST /appointments/
    Body: {
        "delete_list": [1, 2, 3],  # IDs de citas a eliminar (opcional)
        "new_appointments": [...]   # Lista de nuevas citas a crear (opcional)
    }
    
    Returns:
        JsonResponse con el resultado de las operaciones
    """
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Método no permitido. Use POST para gestionar citas.'
        }, status=405)
    
    try:
        # Parsear datos JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {str(e)}")
            return JsonResponse({
                'error': 'JSON inválido en el cuerpo de la solicitud.'
            }, status=400)
        
        delete_ids = data.get('delete_list', [])
        new_appointments_data = data.get('new_appointments', [])
        
        if not delete_ids and not new_appointments_data:
            return JsonResponse({
                'success': False,
                'message': 'No se proporcionaron citas para eliminar ni para crear.',
                'data': {} # Es mejor devolver un diccionario vacío en lugar de un array vacío aquí
            }, status=400) # Un 400 es más apropiado para "Bad Request" o datos insuficientes.

        results = {
            'deleted_count': 0,
            'created_count': 0,
            'errors': []
        }
        
        # Usar transacción atómica para consistencia de datos
        with transaction.atomic():
            # Procesar eliminaciones
            if delete_ids:
                try:
                    results['deleted_count'] = process_appointment_deletion(delete_ids)
                except ValidationError as ve:
                    results['errors'].extend(ve.messages if hasattr(ve, 'messages') else [str(ve)])
            
            # Procesar creaciones
            if new_appointments_data:
                creation_results = process_appointment_creation(new_appointments_data)
                results['created_count'] = creation_results['created_count']
                results['errors'].extend(creation_results['errors'])
        
        # Preparar respuesta
        if not results['errors']:
            return JsonResponse({
                'success': True,
                'message': f"Operación completada exitosamente. "
                          f"Eliminadas: {results['deleted_count']}, "
                          f"Creadas: {results['created_count']}.",
                'data': results
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': "Operación completada con errores. Verifique los detalles.",
                'data': results
            }, status=400)
    
    except Exception as e:
        logger.error(f"Error inesperado en appointments_api: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Error interno del servidor. Consulte los registros para más detalles.'
        }, status=500)
        
        

def process_appointment_deletion(delete_ids: List[int]) -> int:
    """
    Procesa la eliminación de citas médicas.
    
    Args:
        delete_ids: Lista de IDs de citas a eliminar
    
    Returns:
        Número de citas eliminadas
    
    Raises:
        ValidationError: Si los IDs no son válidos
    """
    if not isinstance(delete_ids, list):
        delete_ids = list(delete_ids)
    
    # Validar que todos los IDs sean enteros
    try:
        delete_ids = [int(id_) for id_ in delete_ids if id_]
    except (ValueError, TypeError):
        raise ValidationError("Todos los IDs deben ser números enteros válidos")
    
    if not delete_ids:
        return 0
    
    # Verificar que las citas existan antes de eliminar
    existing_count = CitaMedica.objects.filter(id__in=delete_ids).count()
    if existing_count != len(delete_ids):
        logger.warning(f"Se intentaron eliminar {len(delete_ids)} citas, pero solo {existing_count} existen")
    
    deleted_count, _ = CitaMedica.objects.filter(id__in=delete_ids).delete()
    logger.info(f"Eliminadas {deleted_count} citas con IDs: {delete_ids}")
    
    return deleted_count        


def process_appointment_creation(appointments_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Procesa la creación de múltiples citas médicas.
    
    Args:
        appointments_data: Lista de diccionarios con datos de citas
    
    Returns:
        Diccionario con contadores y errores
    """
    results = {'created_count': 0, 'errors': []}
    
    # Normalizar datos si se recibe un solo objeto
    if not isinstance(appointments_data, list):
        appointments_data = [appointments_data]
    
    for i, appointment_data in enumerate(appointments_data):
        try:
            # Validar datos
            validated_data = validate_appointment_data(appointment_data)
            
            # Obtener objetos relacionados
            paciente: Paciente
            medico: Doctor
            especialidad: Especialidad
            paciente, medico, especialidad = get_related_objects(validated_data)
            
            # Crear cita
            cita = create_appointment(validated_data, paciente, medico, especialidad)
            
            results['created_count'] += 1
            logger.info(f"Cita creada exitosamente: ID {cita.id}, Paciente: {paciente.nombre_completo}, "
                       f"Médico: {medico.nombre_completo}, Fecha: {cita.fecha} {cita.hora_cita}")
            
        except ValidationError as ve:
            error_msg = f"Error de validación en cita #{i+1}: {'; '.join(ve.messages if hasattr(ve, 'messages') else [str(ve)])}"
            results['errors'].append(error_msg)
            logger.warning(error_msg)
            
        except IntegrityError as ie:
            error_msg = f"Error de integridad en cita #{i+1}: {str(ie)}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
            
        except Exception as e:
            error_msg = f"Error inesperado en cita #{i+1}: {str(e)}"
            results['errors'].append(error_msg)
            logger.error(error_msg, exc_info=True)
    
    return results


def validate_appointment_data(appointment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida y normaliza los datos de una cita médica.
    
    Args:
        appointment_data: Diccionario con los datos de la cita
    
    Returns:
        Diccionario con los datos validados y normalizados
    
    Raises:
        ValidationError: Si los datos no son válidos
    """
    errors = []
    validated_data = {}
    
    # Validar campos requeridos
    for field in REQUIRED_APPOINTMENT_FIELDS:
        if not appointment_data.get(field):
            errors.append(f"Campo requerido faltante: {field}")
    
    if errors:
        raise ValidationError(errors)
    
    # Validar y parsear fecha
    fecha_str = appointment_data.get('fecha')
    try:
        fecha = parse_date(fecha_str)
        if not fecha:
            raise ValueError("Formato de fecha inválido")
        validated_data['fecha'] = fecha
    except (ValueError, TypeError):
        errors.append(f"Formato de fecha inválido: {fecha_str}. Use YYYY-MM-DD")
    
    # Validar y parsear hora
    hora_str = appointment_data.get('hora_cita')
    try:
        hora = parse_time(hora_str)
        if not hora:
            raise ValueError("Formato de hora inválido")
        validated_data['hora'] = hora
    except (ValueError, TypeError):
        errors.append(f"Formato de hora inválido: {hora_str}. Use HH:MM")
    
    # Validar IDs numéricos
    try:
        validated_data['paciente_id'] = int(appointment_data.get('paciente_id'))
        validated_data['medico_id'] = int(appointment_data.get('medico_id'))
        
        especialidad_id = appointment_data.get('especialidad_id')
        if especialidad_id:
            validated_data['especialidad_id'] = int(especialidad_id)
    except (ValueError, TypeError) as e:
        errors.append(f"ID inválido: {str(e)}")
    
    # Validar tipo de cita
    tipo_cita_str = appointment_data.get('priority', '').lower()
    tipo_cita_mapping = {
        'normal': TipoCitaChoices.NORMAL,
        'urgente': TipoCitaChoices.URGENTE,
        'seguimiento': TipoCitaChoices.SEGUIMIENTO
    }
    validated_data['tipo_cita'] = tipo_cita_mapping.get(tipo_cita_str, TipoCitaChoices.NORMAL)
    
    # Validar condición si se proporciona
    condicion_str = appointment_data.get('condition')
    if condicion_str:
        valid_conditions = [choice[0] for choice in CondicionPacienteChoices.choices]
        if condicion_str not in valid_conditions:
            logger.warning(f"Condición '{condicion_str}' no válida. Estableciendo a None.")
            condicion_str = None
    validated_data['condicion'] = condicion_str
    
    # Campos opcionales
    validated_data['observaciones'] = appointment_data.get('observaciones', '')
    
    if errors:
        raise ValidationError(errors)
    
    return validated_data


def get_related_objects(validated_data: Dict[str, Any]) -> Tuple[Paciente, Doctor, Especialidad]:
    """
    Obtiene los objetos relacionados (Paciente, Doctor, Especialidad) desde la base de datos.
    
    Args:
        validated_data: Datos validados de la cita
    
    Returns:
        Tupla con (paciente, medico, especialidad)
    
    Raises:
        ValidationError: Si algún objeto no existe
    """
    try:
        paciente = Paciente.objects.select_related().get(id=validated_data['paciente_id'])
    except Paciente.DoesNotExist:
        raise ValidationError(f"Paciente con ID {validated_data['paciente_id']} no encontrado")
    
    try:
        medico = Doctor.objects.select_related().get(id=validated_data['medico_id'])
    except Doctor.DoesNotExist:
        raise ValidationError(f"Médico con ID {validated_data['medico_id']} no encontrado")
    
    especialidad = None
    if validated_data.get('especialidad_id'):
        try:
            especialidad = Especialidad.objects.get(id=validated_data['especialidad_id'])
        except Especialidad.DoesNotExist:
            raise ValidationError(f"Especialidad con ID {validated_data['especialidad_id']} no encontrada")
    
    return paciente, medico, especialidad


def create_appointment(validated_data: Dict[str, Any], paciente: Paciente, 
                      medico: Doctor, especialidad: Especialidad = None) -> CitaMedica:
    """
    Crea una nueva cita médica.
    
    Args:
        validated_data: Datos validados de la cita
        paciente: Objeto Paciente
        medico: Objeto Doctor
        especialidad: Objeto Especialidad (opcional)
    
    Returns:
        CitaMedica: Objeto de la cita creada
    
    Raises:
        IntegrityError: Si hay conflictos de integridad en la base de datos
    """
    # Verificar disponibilidad del médico
    existing_appointment = CitaMedica.objects.filter(
        medico =medico,
        fecha=validated_data['fecha'],
        hora_cita=validated_data['hora'],
        estado__in=[EstadoCitaChoices.OCUPADO, EstadoCitaChoices.OCUPADO]
    ).first()
    
    if existing_appointment:
        raise IntegrityError(
            f"El médico {medico.nombre_completo} ya tiene una cita programada para "
            f"{validated_data['fecha']} a las {validated_data['hora']}"
        )
    
    cita = CitaMedica.objects.create(
        paciente=paciente,
        medico=medico,
        fecha=validated_data['fecha'],
        hora_cita=validated_data['hora'],
        estado=EstadoCitaChoices.OCUPADO,
        observaciones=validated_data['observaciones'],
        condicion=validated_data['condicion'],
        especialidad=especialidad,
        tipo_cita=validated_data['tipo_cita']
    )
    
    return cita



@login_required
def get_appointments_api(request):
   
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido. Use GET.'}, status=405)

    try:
        # Obtener los parámetros de fecha del request
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        print('llegue al servidor...', start_date_str, end_date_str)
        # Validar y convertir las fechas
        if not start_date_str or not end_date_str:
            return JsonResponse({'error': 'Faltan parámetros de fecha (start_date, end_date).'}, status=400)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido. Use YYYY-MM-DD.'}, status=400)

        # Consultar citas dentro del rango de fechas
        # Usamos select_related para traer los datos relacionados (Paciente, Doctor, Especialidad)
        # en una sola consulta, evitando N+1 queries.
        citas = CitaMedica.objects.select_related('paciente', 'medico', 'especialidad').filter(
            fecha__range=[start_date, end_date]
        ).order_by('fecha', 'hora_cita')

        # Serializar los datos de las citas
        serialized_citas = []
        for cita in citas:
            # Mapear los choices de Django a un formato amigable para el frontend si es necesario.
            # Por ejemplo, TipoCitaChoices.NORMAL.value devuelve 'normal'.
            tipo_cita_display = cita.get_tipo_cita_display() # Obtiene la representación legible del choice
            condicion_display = cita.get_condicion_display() if cita.condicion else None

            serialized_citas.append({
                'id': cita.id,
                'paciente_id': cita.paciente.id,
                'patientName': f"{cita.paciente.nombres} {cita.paciente.apellidos}", # Nombre completo del paciente
                'medico_id': cita.medico.id if cita.medico else None,
                'medicoName': f"{cita.medico.nombres} {cita.medico.apellidos}" if cita.medico else None,
                'especialidad_id': cita.especialidad.id if cita.especialidad else None,
                'especialidadName': cita.especialidad.nombre if cita.especialidad else None,
                'fecha': cita.fecha.isoformat(), # Formato 'YYYY-MM-DD'
                'hora_cita': cita.hora_cita.strftime('%H:%M'), # Formato 'HH:MM'
                'estado': cita.estado,
                'condicion': cita.condicion, # Guardar el valor real del choice
                'condicionDisplay': condicion_display, # Guardar el valor legible del choice
                'observaciones': cita.observaciones,
                'tipo_cita': cita.tipo_cita, # Guardar el valor real del choice (e.g., 'normal', 'urgente')
                'tipoCitaDisplay': tipo_cita_display, # Guardar el valor legible del choice
            })

        return JsonResponse({
            'success': True,
            'message': 'Citas obtenidas exitosamente.',
            'data': serialized_citas
        }, status=200)

    except Exception as e:
        logger.error(f"Error inesperado en get_appointments_api: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Error interno del servidor. Consulte los registros.'}, status=500)

