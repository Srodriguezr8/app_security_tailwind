

import json
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from applications.security.models import Group, Menu, Module
from django.urls import reverse


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
    
    

@login_required
def get_group_menus(request):
    """
    Vista AJAX para obtener los menús de un grupo específico
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
        
    try:
        data = json.loads(request.body)
        group_id = data.get('group_id')
        
        # Si no hay group_id, devolver menús vacíos
        if not group_id:
            return JsonResponse({
                'success': True,
                'menus': []
            })
            

        # Obtener el grupo
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Grupo no encontrado'}, status=404)
        
        # Verificar que el usuario tenga acceso a este grupo
        if not request.user.groups.filter(id=group_id).exists():
            return JsonResponse({'error': 'Sin permisos para este grupo'}, status=403)
            
         # Obtener los menús del grupo
        menus = Menu.objects.filter(
            modules__group_permissions__group=group,
            modules__is_active=True
        ).distinct().order_by('order', 'name')
        
        menu_list = _serialize_menus_with_modules(menus, group)
        
        print('-----------------------------------')
        for item in menu_list:
            print('itesm:', item)
            
        return JsonResponse({
            'success': True,
            'menus': menu_list
        })
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"[ERROR] Error en get_group_menus: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    
    

def _serialize_menus_with_modules(menus, group):
    """
    Función auxiliar para serializar menús con sus módulos filtrados por grupo
    """
    menu_list = []
    for menu in menus:
        # Obtener módulos activos del menú que pertenezcan al grupo
        modules = menu.modules.filter(
            group_permissions__group=group,
            is_active=True
        ).distinct().order_by('order', 'name')
        
        module_list = []
        for module in modules:
            try:
                url = f"/{module.url}" if not module.url.startswith('/') else module.url
            except:
                url = '#'
                
            module_list.append({
                'id': module.id,
                'name': module.name,
                'url': url,
                'icon': module.icon,
                'order': module.order,
                'description': module.description or ''
            })
        
        # Solo agregar el menú si tiene módulos
        if module_list:
            menu_list.append({
                'id': menu.id,
                'name': menu.name,
                'icon': menu.icon,
                'order': menu.order,
                'modules': module_list
            })
            
    return menu_list


def _serialize_all_menus(menus):
    """
    Función auxiliar para serializar todos los menús con todos sus módulos (para superusuarios)
    """
    menu_list = []
    for menu in menus:
        # Obtener todos los módulos activos del menú
        modules = menu.modules.filter(is_active=True).order_by('order', 'name')
        
        module_list = []
        for module in modules:
            try:
                url = f"/{module.url}" if not module.url.startswith('/') else module.url
            except:
                url = '#'
                
            module_list.append({
                'id': module.id,
                'name': module.name,
                'url': url,
                'icon': module.icon,
                'order': module.order,
                'description': module.description or ''
            })
        
        # Solo agregar el menú si tiene módulos
        if module_list:
            menu_list.append({
                'id': menu.id,
                'name': menu.name,
                'icon': menu.icon,
                'order': menu.order,
                'modules': module_list
            })
            
    return menu_list

def test_group_menus(request):
    """Vista de prueba que siempre devuelve datos"""
    return JsonResponse({
        'success': True,
        'menus': [
            {
                'id': 99,
                'name': 'Menú de Prueba Simple',
                'url_name': 'simple_test',
                'url': '#simple-test',
                'icon_path': 'M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zm0-8h14V7H7v2z',
                'order': 1
            }
        ],
        'message': 'Vista de prueba funcionando correctamente'
    })
    
