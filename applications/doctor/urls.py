from django.urls import path

from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, \
    AtencionDeleteView
from applications.doctor.views.pago import ( PagoListView, PagoCreateView, PagoUpdateView, PagoDeleteView)
app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),
    
    # Rutas para pago
    path('pagos/', PagoListView.as_view(), name="pago_list"),
    path('pagos/nuevo/', PagoCreateView.as_view(), name="pago_create"),
    path('pagos/editar/<int:pk>/', PagoUpdateView.as_view(), name="pago_update"),
    path('pagos/eliminar/<int:pk>/', PagoDeleteView.as_view(), name="pago_delete"),
]