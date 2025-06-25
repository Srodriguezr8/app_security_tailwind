

import json
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from applications.security.models import GroupModulePermission, Module, User,Group
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,TemplateView
from django.db.models import Q

class GroupModulePermissionListView(TemplateView):
    template_name = 'security/group_module_permission/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['modules'] = Module.objects.all()
        return context




class GroupModulePermissionPermissionsView(View):
    def get(self, request, *args, **kwargs):
        try:
            group_id = request.GET.get('group_id')
            module_id = request.GET.get('module_id')
            gmp = GroupModulePermission.objects.get(group_id=group_id, module_id=module_id)
            permissions = list(gmp.permissions.values('id', 'name'))

            return JsonResponse({'permissions': permissions, 'count_permission':len(permissions)})
        
        except GroupModulePermission.DoesNotExist:
            return JsonResponse({'permissions': []})
    
        
class PemissionsModuleView(DetailView):
    model= Module
    def get(self, request,*args,**kargs):

        try:
            obj = self.get_object()
            permissions = list(obj.permissions.values('id', 'name'))
            return JsonResponse({'modules':permissions})
        except Exception:
            return JsonResponse({'error':f'No se han encontrado los permisos del modulo {obj.name}'},status = 404)


class SaveGroupModulePermissionView(View):
    def post(self,request,*args,**kgars):
        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            module_id =  data.get('module_id')
            permissions = data.get('permissions',[])

            group = Group.objects.filter(pk = group_id).first()
            module = Module.objects.filter(pk = module_id).first()

            gmp, created = GroupModulePermission.objects.get_or_create(group=group, module=module)

            gmp.permissions.clear()

            if permissions:
                gmp.permissions.add(*permissions)

            response = {'success': 'Permisos asignados correctamente',
                        'is_created':created}

            return JsonResponse(response)
        except:
            return JsonResponse({'error': 'Error al guardar los permisos'})

class DeleteGroupModulePermissionView(View):
    def post(self,request,*args,**kargs):

        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            module_id =  data.get('module_id')

            delete_count, _ = GroupModulePermission.objects.filter(group_id = group_id, module_id = module_id).delete()

            if delete_count==0:
                return JsonResponse({
                    'message': 'No existe nada que eliminar',
                    'status': 'not_found'
                })

            return JsonResponse({
                    'message': ' Se han eliminado correctamente los permisos del módulo del grupo',
                    'status': 'deleted'
                })
        except Exception:
            return JsonResponse({'error': 'Error al eliminar'},status=400)
        
