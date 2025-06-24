

from django.views.generic import TemplateView
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin

class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context={}
        context["title"]= "IC - Modulos"
        context["title1"]= "Modulos Disponibles"
        MenuModule(self.request).fill(context)
        
         # Si no hay grupo actual pero hay grupos disponibles, selecciona el primero
        if not context.get("group") and context.get("group_list"):
            context["group"] = context["group_list"].first()
        
        # print("estoy saliendo en el modulo template view")
        # print("MENUS:", context.get("menu_list"))
        # print("GRUPOS:", context.get("group_list"))
        # print("GRUPO ACTUAL:", context.get("group"))
        return context
    
    
class StartTemplateView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        context={}
        context["title"]= "IC - Modulos"
        context["title1"]= "Modulos Disponibles"
        MenuModule(self.request).fill(context)
        
        print("estoy saliendo en el modulo template view")
       
        return context
    
    
