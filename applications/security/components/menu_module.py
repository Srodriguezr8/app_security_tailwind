from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest

from applications.security.models import GroupModulePermission, User
from applications.security.models import Module, Menu
from django.urls import reverse


class MenuModule:
    def __init__(self, request: HttpRequest):
        self._request = request
        self._path = self._request.path

    def fill(self, data):
        try:
            data['user'] = self._request.user
            data['date_time'] = datetime.now()
            data['date_date'] = datetime.now().date()

            if not self._request.user.is_authenticated or self._request.method != 'GET':
                return

            data['group_list'] = self._request.user.groups.all().order_by('id')

            # SUPERUSUARIO: acceso a todos los menús
            if self._request.user.is_superuser:
                data['menu_list'] = self.__get_superuser_menu_list()
                return

            # Si no hay grupo en sesión y existen grupos, selecciona el primero
            if 'group_id' not in self._request.session:
                if data['group_list'].exists():
                    self._request.session['group_id'] = data['group_list'].first().id

            # Si viene?gpid= en la URL, actualiza el grupo en sesión
            group_id = self._request.GET.get('gpid')
            if group_id:
                try:
                    self._request.session['group_id'] = int(group_id)
                except (ValueError, TypeError):
                    pass  # Ignorar errores de conversión

            # Si hay un grupo en sesión, cargarlo como `group`
            if self._request.session.get('group_id'):
                try:
                    group = Group.objects.get(id=self._request.session['group_id'])
                    data['group'] = group
                    data['menu_list'] = self.__get_menu_list(data["user"], group)
                except Group.DoesNotExist:
                    data['group'] = None
                    data['menu_list'] = []
            else:
                # Como fallback, si aún no hay grupo y sí hay lista, asignar el primero
                if data['group_list'].exists():
                    group = data['group_list'].first()
                    data['group'] = group
                    self._request.session['group_id'] = group.id
                    data['menu_list'] = self.__get_menu_list(data["user"], group)
                else:
                    data['group'] = None
                    data['menu_list'] = []

        except Exception as ex:
            print(f"[ERROR] Error al llenar menú: {ex}")
            data['menu_list'] = []

    def __get_superuser_menu_list(self):
        """
        Obtiene todos los menús para superusuarios
        """
        try:
            menus = Menu.objects.filter(
                modules__is_active=True
            ).distinct().order_by('order', 'name')
            
            return self.__serialize_all_menus(menus)
        except Exception as ex:
            print(f"[ERROR] Error al obtener menús de superusuario: {ex}")
            return []

    def __serialize_all_menus(self, menus):
        """
        Serializa todos los menús con todos sus módulos activos (para superusuarios)
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

    def __get_menu_list(self, user, group):
        """
        Obtiene los menús filtrados por grupo y permisos del usuario
        """
        try:
            # Obtener menús que tienen módulos asignados al grupo
            menus = Menu.objects.filter(
                modules__group_permissions__group=group,
                modules__is_active=True
            ).distinct().order_by('order', 'name')
            
            return self.__serialize_menus_with_modules(menus, group)
        except Exception as ex:
            print(f"[ERROR] Error al obtener menús del grupo: {ex}")
            return []

    def __serialize_menus_with_modules(self, menus, group):
        """
        Serializa los menús con sus módulos filtrados por grupo
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
                    # Intentar generar la URL
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

    def __serialize_menus(self, menus):
        """
        Serializa los menús a formato dict
        """
        menu_list = []
        for menu in menus:
            try:
                # Intentar generar la URL
                url = reverse(menu.url_name) if menu.url_name else '#'
            except:
                # Si falla, usar una URL por defecto
                url = '#'
                
            menu_list.append({
                'id': menu.id,
                'name': menu.name,
                'url_name': menu.url_name,
                'url': url,
                'icon_path': menu.icon_path if hasattr(menu, 'icon_path') else '',
                'order': menu.order if hasattr(menu, 'order') else 0
            })
            
        return menu_list

    # Método público para usar en las vistas
    def get_menu_list_for_group(self, user, group):
        """
        Método público para obtener menús de un grupo específico
        """
        if user.is_superuser:
            return self.__get_superuser_menu_list()
        else:
            return self.__get_menu_list(user, group)


                
                