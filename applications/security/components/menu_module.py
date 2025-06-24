from datetime import datetime
from django.contrib.auth.models import Group
from django.http import HttpRequest

from applications.security.models import GroupModulePermission, User
from applications.security.models import Module, Menu



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

            # Si viene ?gpid= en la URL, actualiza el grupo en sesión
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
