from django.urls import path

from applications.doctor.views.agenda_cita import AgendaCitaMedicaListView, add_patient_api, patients_search_api, add_appointments_api,get_appointments_api, get_doctors_api, get_setting_hours
from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView,AtencionDeleteView
from applications.doctor.views.pago import ( PagoListView, PagoCreateView, PagoUpdateView, PagoDeleteView)
app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    
  # Citas
    path('agenda_cita/', AgendaCitaMedicaListView.as_view(), name="agenda_cita"),
    path('patient_create_api/', add_patient_api, name="patient_create_api"),   # crea nueve paciente desde panel de agendar
    path('patients_search_api/', patients_search_api, name="patients_search_api"),  # busca pacientes 
    path('appointments_create_api/', add_appointments_api, name="appointments_create_api"),
    path('appointments_list/', get_appointments_api, name="appointments_list"),
    path('doctors_list/', get_doctors_api, name="doctors_list"),
    path('setting_hours_list/', get_setting_hours, name="setting_hours_list"),
    
    # Rutas para pago
    path('pagos/', PagoListView.as_view(), name="pago_list"),
    path('pagos/nuevo/', PagoCreateView.as_view(), name="pago_create"),
    path('pagos/editar/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('pagos/eliminar/<int:pk>/', PagoDeleteView.as_view(), name="pago_delete"),
]