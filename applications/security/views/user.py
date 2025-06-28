import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import SessionGroupMixin, UpdateViewMixin, ListViewMixin, PermissionMixin
from applications.security.forms.user import UserForm, UserStatusForm
from applications.security.models import User
from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate, get_user_model

User = get_user_model()

class UserListView( SessionGroupMixin, PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/users/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'view_user'
    paginate_by = 10 # Asegúrate de que ListViewMixin o aquí se define la paginación

    def get_queryset(self):
        q = self.request.GET.get("q")
        queryset = super().get_queryset()

        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(email__icontains=q) # Asegúrate de que 'email' es el campo correcto
            ).distinct() # Añade .distinct() para evitar duplicados si hay múltiples coincidencias

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios'
        # Asegúrate que reverse_lazy 'security:user_update' existe y es lo que quieres para el create_url
        context['create_url'] = reverse_lazy('security:user_update', args=[self.request.user.id]) 
        context['title1'] = 'Gestión de Usuarios'
        # Añadir 'request' al contexto para usar en los templates
        context['request'] = self.request 
        # Asegúrate de que 'permissions' se pasa correctamente
        # context['permissions'] = self.request.user.get_all_permissions() # O tu lógica de permisos
        # Para que el mixin de permisos funcione con el context de la vista
        if hasattr(self.request.user, 'get_all_permissions'):
            context['permissions'] = self.request.user.get_all_permissions()
        else:
            context['permissions'] = self.request.user.get_user_permissions() # O Default
         
        print("Contenido de menu_list:",context['menu_list'])
        print("Tipo de menu_list:", type(context['menu_list']))
            
        return context

    def render_to_response(self, context, **response_kwargs):
        # Detectar si la solicitud es AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Si es AJAX, renderiza solo las partes que cambian y devuélvelas como JSON
            # Asegúrate de pasar el 'page_obj' a los contextos de los sub-parciales
            # ListView ya pasa 'page_obj' en el contexto, pero aquí lo necesitas directamente
            page_obj = context['page_obj']
            users = page_obj.object_list # La lista de usuarios de la página actual

            # Crea un nuevo contexto específico para los sub-parciales si es necesario,
            # pero el 'context' completo ya debería contener 'page_obj', 'users', 'request', 'permissions'.
            # Revisa que 'users' en los sub-parciales se refiera a 'page_obj.object_list'
            # para asegurar que solo se pasen los usuarios de la página actual.
            
            # Pasar 'page_obj', 'users', 'request', 'permissions' y 'request' explícitamente si no están bien en context
            sub_context = {
                'users': users,
                'page_obj': page_obj,
                'request': self.request,
                'permissions': context.get('permissions', []), # Asegura que permissions está presente
            }
            
            table_body_html = render_to_string('security/users/user_table_body.html', sub_context, request=self.request)
            pagination_html = render_to_string('security/users/user_pagination_nav.html', sub_context, request=self.request)
            
            return JsonResponse({
                'table_body_html': table_body_html,
                'pagination_html': pagination_html,
            })
        else:
            # Si no es AJAX, renderiza el parcial completo
            return super().render_to_response(context, **response_kwargs)
    
    

class UserUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    template_name = 'security/users/form.html'
    form_class = UserForm
    success_url = reverse_lazy('security:user_list')
    permission_required = 'change_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Usuario'
        context['back_url'] = self.success_url
        context['title'] = 'Actualizar Usuario'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Éxito al actualizar el usuario {user.last_name}.")
        return response
    

@csrf_exempt
def toggle_user_status(request, user_id):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            is_active = data.get('is_active')
            
            user = User.objects.get(pk=user_id)

            # Evitar que el usuario se desactive a sí mismo
            if user == request.user:
                return JsonResponse({
                    'success': False,
                    'error': 'No puedes desactivarte a ti mismo.'
                })

            user.is_active = is_active
            user.save()

            return JsonResponse({
                'success': True,
                'is_active': user.is_active,
                'message': f"Estado actualizado correctamente. Ahora el usuario está {'activo' if user.is_active else 'inactivo'}."
            })

        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no encontrado.'
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido.'
        })


def user_list_view(request):
    # Lógica de filtrado y paginación (esto ya lo tienes)
    search_query = request.GET.get('q', '')
    users_list = User.objects.all()
    if search_query:
        users_list = users_list.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) | 
            Q(email__icontains=search_query)
        ).distinct()

    paginator = Paginator(users_list, 10) # 10 usuarios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print('vien filtrado', users_list)
    # Contexto que se pasaría a los templates
    context = {
        'title1': 'Gestión de Usuarios',
        'users': page_obj.object_list, # Pasa solo los usuarios de la página actual
        'page_obj': page_obj,
        'request': request, # Importante para las URLs en los templates
        'permissions': request.user.get_all_permissions(), # O tu lógica de permisos
    }


    # Detectar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print('va entrar a ajaz-------------------')
            # Si es AJAX (desde fetchUsers en user_list_partial.html), devuelve JSON
            table_body_html = render_to_string('security/users/user_table_body.html', context, request=request)
            pagination_html = render_to_string('security/users/user_pagination_nav.html', context, request=request)

            return JsonResponse({
                'table_body_html': table_body_html,
                'pagination_html': pagination_html,
            })
    else:
        # Si NO es AJAX (desde loadContent en base.html), devuelve el parcial HTML completo
        return render(request, 'security/users/user_list_partial.html', context)
    
    


