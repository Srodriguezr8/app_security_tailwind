from django.urls import path
from applications.core.views.cargo import CargoCreateView, CargoDeleteView, CargoListView, CargoUpdateView
from applications.core.views.diagnostico import DiagnosticoCreateView, DiagnosticoDeleteView, DiagnosticoListView, DiagnosticoUpdateView
from applications.core.views.doctor import DoctorCreateView, DoctorDeleteView, DoctorListView, DoctorUpdateView, EspecialidadDoctorView
from applications.core.views.paciente import paciente_find

app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Pacientes
    path('paciente_find/', paciente_find, name="paciente_find"),

    # Rutas  para vistas relacionadas con cargos
    path('cargo_list/',CargoListView.as_view() ,name="cargo_list"),
    path('cargo_create/', CargoCreateView.as_view(),name="cargo_create"),
    path('cargo_update/<int:pk>/', CargoUpdateView.as_view(),name='cargo_update'),
    path('cargo_delete/<int:pk>/', CargoDeleteView.as_view(),name='cargo_delete'),

    # Rutas  para vistas relacionadas con diagnosticos
    path('diagnostico_list/',DiagnosticoListView.as_view() ,name="diagnostico_list"),
    path('diagnostico_create/', DiagnosticoCreateView.as_view(),name="diagnostico_create"),
    path('diagnostico_update/<int:pk>/', DiagnosticoUpdateView.as_view(),name='diagnostico_update'),
    path('diagnostico_delete/<int:pk>/', DiagnosticoDeleteView.as_view(),name='diagnostico_delete'),

     # Rutas  para vistas relacionadas con doctores
    path('doctor_list/',DoctorListView.as_view() ,name="doctor_list"),
    path('doctor_create/', DoctorCreateView.as_view(),name="doctor_create"),
    path('doctor_update/<int:pk>/', DoctorUpdateView.as_view(),name='doctor_update'),
    path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(),name='doctor_delete'),
    path('doctor/<int:pk>/especialidades/', EspecialidadDoctorView.as_view(),name='doctor_especialidades'),


]