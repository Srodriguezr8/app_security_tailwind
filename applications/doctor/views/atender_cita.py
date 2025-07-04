
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, date
from applications.core.models import Doctor
from applications.doctor.models import CitaMedica
import json

from django.contrib.auth import get_user_model

User = get_user_model()

class CalendarioMedicoView( ListView):
    template_name = 'doctor/citas/calendario_medico.html'
    model = CitaMedica
    context_object_name = 'citas'
    
    def get_queryset(self):
        # Obtener el doctor actual (asumiendo que el usuario logueado es un doctor)
        try:
            doctor = Doctor.objects.filter(pk=3).first()
        except Doctor.DoesNotExist:
            return CitaMedica.objects.none()
        
        # Obtener la fecha actual y calcular el rango de la semana
        today = timezone.now().date()
        
        # Si se pasa una fecha específica en la URL, usarla
        fecha_param = self.request.GET.get('fecha')
        if fecha_param:
            try:
                today = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Calcular el lunes de la semana actual
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        sunday = monday + timedelta(days=6)
        
        # Filtrar citas del doctor para la semana actual
        return CitaMedica.objects.filter(
            medico=doctor,
            fecha__range=[monday, sunday]
        ).select_related('paciente', 'especialidad').order_by('fecha', 'hora_cita')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el doctor actual
        try:
            doctor = Doctor.objects.filter(pk=3).first()
            context['doctor'] = doctor
        except Doctor.DoesNotExist:
            context['doctor'] = None
            return context
        
        # Calcular fechas de la semana
        today = timezone.now().date()
        fecha_param = self.request.GET.get('fecha')
        if fecha_param:
            try:
                today = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        
        # Crear lista de días de la semana
        dias_semana = []
        nombres_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        
        for i in range(7):
            fecha_dia = monday + timedelta(days=i)
            dias_semana.append({
                'nombre': nombres_dias[i],
                'fecha': fecha_dia,
                'es_hoy': fecha_dia == timezone.now().date(),
                'citas': []
            })
        
        # Organizar citas por día
        citas = self.get_queryset()
        for cita in citas:
            dia_index = cita.fecha.weekday()
            if 0 <= dia_index <= 6:
                dias_semana[dia_index]['citas'].append(cita)
        
        context['dias_semana'] = dias_semana
        context['semana_actual'] = monday
        context['semana_siguiente'] = monday + timedelta(days=7)
        context['semana_anterior'] = monday - timedelta(days=7)
        context['hoy'] = timezone.now().date()
        
        return context

def obtener_citas_ajax(request):
    """Vista AJAX para obtener citas de una fecha específica"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autorizado'}, status=401)
    
    try:
        doctor = Doctor.objects.filter(pk=3).first()
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor no encontrado'}, status=404)
    
    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return JsonResponse({'error': 'Fecha requerida'}, status=400)
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
    
    citas = CitaMedica.objects.filter(
        medico=doctor,
        fecha=fecha
    ).select_related('paciente', 'especialidad').order_by('hora_cita')
    
    citas_data = []
    for cita in citas:
        citas_data.append({
            'id': cita.id,
            'paciente': cita.paciente.nombre_completo,
            'hora': cita.hora_cita.strftime('%H:%M'),
            'especialidad': cita.especialidad.nombre if cita.especialidad else '',
            'estado': cita.get_estado_display(),
            'estado_class': cita.estado,
            'tipo_cita': cita.get_tipo_cita_display(),
            'condicion': cita.get_condicion_display() if cita.condicion else '',
            'observaciones': cita.observaciones or ''
        })
    
    return JsonResponse({'citas': citas_data})