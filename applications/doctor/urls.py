from django.urls import path

from applications.doctor.views.agenda_cita import AgendaCitaMedicaListView, add_patient_api, patients_search_api
from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView
from applications.doctor.views.servicio_adicional import ServicioAdicionalCreateView, ServicioAdicionalDeleteView, ServicioAdicionalListView, ServicioAdicionaloUpdateView

app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    
  # Citas
    path('agenda_cita/', AgendaCitaMedicaListView.as_view(), name="agenda_cita"),
    path('patient_create_api/', add_patient_api, name="patient_create_api"),
    path('patients_search_api/', patients_search_api, name="patients_search_api"),


    # Rutas  para vistas relacionadas con Doctor
    path('servicio_adicional_list/', ServicioAdicionalListView.as_view(), name="servicio_adicional_list"),
    path('servicio_adicional_create/', ServicioAdicionalCreateView.as_view(), name="servicio_adicional_create"),
    path('servicio_adicional_update/<int:pk>/', ServicioAdicionaloUpdateView.as_view(), name="servicio_adicional_update"),
    path('servicio_adicional_delete/<int:pk>/', ServicioAdicionalDeleteView.as_view(), name="servicio_adicional_delete"),
]