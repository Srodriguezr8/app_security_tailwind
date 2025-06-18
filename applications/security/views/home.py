

from django.views.generic import TemplateView
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin

class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'home.html'
    print ('agerherhrthtrjytyjyt')
    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context={}
        context["title"]= "IC - Modulos"
        context["title1"]= "Modulos Disponibles"
        MenuModule(self.request).fill(context)
        
        print("estoy saliendo en el modulo template view")
       
        return context
    
class PublicDashboardView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'clinic_name': 'Clinica Medica S.A.',
        'mission': 'Brindar atención médica de calidad...',
        'vision': 'Ser líder en servicios médicos...',
        'contact': 'info@clinica.com | +593 987654321',
        'specialties': ['Cardiología', 'Pediatría', 'Dermatología'],
        'doctors': [
            {'name': 'Dr. Juan Pérez', 'specialty': 'Cardiología'},
            {'name': 'Dr. María Gómez', 'specialty': 'Pediatría'},
        ]
    }