from django.urls import path

from applications.doctor.views.agenda_cita import (
    AgendaCitaMedicaListView,
    add_patient_api,
    patients_search_api,
    add_appointments_api,
    get_appointments_api,
    get_doctors_api,
    get_setting_hours
)
from applications.doctor.views.atencion_medica import (
    AtencionListView,
    AtencionCreateView,
    AtencionUpdateView,
    AtencionDeleteView
)
from applications.doctor.views.pago import (
    PagoListView,
    PagoCreateView,
    PagoUpdateView,
    PagoDeleteView
)
from applications.doctor.views.servicio_adicional import (
    ServicioAdicionalCreateView,
    ServicioAdicionalDeleteView,
    ServicioAdicionalListView,
    ServicioAdicionaloUpdateView
)
from applications.doctor.views.ordenpago import (
    OrdenPagoCreateView,
    crear_servicio_adicional,
    get_valor_consulta,
    get_costo_servicio_adicional,
    guardar_detalle_pago,
    detalles_pago_tbody_ajax,
)

app_name = 'doctor'  # define un espacio de nombre para la aplicación

urlpatterns = [
    # Rutas para vistas relacionadas con Atenciones Médicas
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Rutas para Citas
    path('agenda_cita/', AgendaCitaMedicaListView.as_view(), name="agenda_cita"),
    path('patient_create_api/', add_patient_api, name="patient_create_api"),
    path('patients_search_api/', patients_search_api, name="patients_search_api"),
    path('appointments_create_api/', add_appointments_api, name="appointments_create_api"),
    path('appointments_list/', get_appointments_api, name="appointments_list"),
    path('doctors_list/', get_doctors_api, name="doctors_list"),
    path('setting_hours_list/', get_setting_hours, name="setting_hours_list"),

    # Rutas para pagos
    path('pagos/', PagoListView.as_view(), name="pago_list"),
    path('pagos/nuevo/', PagoCreateView.as_view(), name="pago_create"),
    path('pagos/editar/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('pagos/eliminar/<int:pk>/', PagoDeleteView.as_view(), name="pago_delete"),

    # Rutas para servicios adicionales
    path('servicio_adicional_list/', ServicioAdicionalListView.as_view(), name="servicio_adicional_list"),
    path('servicio_adicional_create/', ServicioAdicionalCreateView.as_view(), name="servicio_adicional_create"),
    path('servicio_adicional_update/<int:pk>/', ServicioAdicionaloUpdateView.as_view(), name="servicio_adicional_update"),
    path('servicio_adicional_delete/<int:pk>/', ServicioAdicionalDeleteView.as_view(), name="servicio_adicional_delete"),

    # Orden de pago
    path('pagos/crear/', OrdenPagoCreateView.as_view(), name='pagos_crear'),

    # API Servicio adicional
    path('api/servicio_adicional/crear/', crear_servicio_adicional, name='crear_servicio_adicional'),
    path('api/get_valor_consulta/<int:pago_id>/', get_valor_consulta, name='get_valor_consulta'),
    path('api/get_costo_servicio/<int:servicio_id>/', get_costo_servicio_adicional, name='get_costo_servicio'),
    path('api/guardar_detalle_pago/', guardar_detalle_pago, name='guardar_detalle_pago'),
        #Orden de pago
    path('pagos/crear/', OrdenPagoCreateView.as_view(), name='pagos_crear'),
    #API SERVICIO ADICIONAL
    path('api/servicio_adicional/crear/', crear_servicio_adicional, name='crear_servicio_adicional'),
    #Api MONTO TOTAL
    path('api/get_valor_consulta/<int:pago_id>/', get_valor_consulta, name='get_valor_consulta'),
    #API AUTOMATIZACION SERVICIO ADICIONAL
    path('api/get_costo_servicio/<int:servicio_id>/', get_costo_servicio_adicional, name='get_costo_servicio'),
    #API GUARDAR DETALLE PAGO
    path('api/guardar_detalle_pago/', guardar_detalle_pago, name='guardar_detalle_pago'),
    #AJAX DETALLE DE PAGO
    path('api/detalles_pago/<int:pago_id>/', detalles_pago_tbody_ajax, name='detalles_pago_tbody_ajax'),

]
