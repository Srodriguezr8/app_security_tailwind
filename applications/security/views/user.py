import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import SessionGroupMixin, UpdateViewMixin, ListViewMixin, PermissionMixin
from applications.security.forms.user import UserForm, UserStatusForm
from applications.security.models import User
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

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
        # es posible obtnener estsa lita    
        # permissions = self.request.user.get_all_permissions()
   
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
    
    

class UserCreateView(SessionGroupMixin, PermissionMixin, CreateView):
    model = User
    template_name = 'security/users/create.html'  # Mismo template
    permission_required = 'add_user'
    success_url = reverse_lazy('security:user_list')
    
    fields = [
        'username', 'email', 'first_name', 'last_name', 
        'dni', 'phone', 'direction', 'image', 'is_active'
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Usuario'
        context['title1'] = 'Nuevo Usuario'
        context['cancel_url'] = reverse_lazy('security:user_list')
        context['is_edit'] = False  # Flag para saber si estamos creando
        return context


class UserUpdateView(SessionGroupMixin, PermissionMixin, UpdateView):
    model = User
    template_name = 'security/users/create.html'  # Usaremos el mismo template
    permission_required = 'change_user'
    success_url = reverse_lazy('security:user_list')
    
    fields = [
        'username', 'email', 'first_name', 'last_name', 
        'dni', 'phone', 'direction', 'image', 'is_active'
    ]
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['title1'] = 'Editar Usuario'
        context['cancel_url'] = reverse_lazy('security:user_list')
        context['is_edit'] = True  # Flag para saber si estamos editando
        context['user_obj'] = self.object  # Objeto usuario para el template
        return context
    
    def form_valid(self, form):
        try:
            # No modificamos la contraseña en la edición
            # La contraseña se mantiene igual a menos que se use otra vista específica
            
            response = super().form_valid(form)
            
            messages.success(
                self.request, 
                f'Usuario {form.instance.get_full_name} actualizado exitosamente.'
            )
            return response
            
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar usuario: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)



class UserDeleteView(SessionGroupMixin, PermissionMixin, DeleteView):
    model = User
    template_name = 'security/users/delete.html'
    permission_required = 'delete_user'
    success_url = reverse_lazy('security:user_list')
    context_object_name = 'user_obj'
    
    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuario'
        context['title1'] = 'Confirmar Eliminación'
        context['cancel_url'] = reverse_lazy('security:user_list')
        
        # Verificar si el usuario tiene datos relacionados
        user = self.object
        context['has_related_data'] = self.check_related_data(user)
        context['related_info'] = self.get_related_info(user)
        
        return context
    
    def check_related_data(self, user):
        """Verificar si el usuario tiene datos relacionados que impedirían la eliminación"""
        # Aquí puedes agregar verificaciones según tu modelo
        # Por ejemplo, si tiene posts, comentarios, etc.
        related_data = False
        
        # Ejemplo de verificaciones:
        # if user.posts.exists():
        #     related_data = True
        # if user.comments.exists():
        #     related_data = True
        
        return related_data
    
    def get_related_info(self, user):
        """Obtener información sobre datos relacionados"""
        info = []
        
        # Ejemplo de información relacionada:
        # if user.posts.exists():
        #     info.append(f"{user.posts.count()} publicaciones")
        # if user.comments.exists():
        #     info.append(f"{user.comments.count()} comentarios")
        
        return info
    
    def delete(self, request, *args, **kwargs):
        """Sobrescribir el método delete para manejar la eliminación"""
        self.object = self.get_object()
        
        # Verificar que no sea el usuario actual
        if self.object == request.user:
            messages.error(request, 'No puedes eliminar tu propia cuenta.')
            return redirect(self.success_url)
        
        # Verificar si es superusuario (opcional)
        if self.object.is_superuser and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para eliminar un superusuario.')
            return redirect(self.success_url)
        
        try:
            user_name = self.object.get_full_name
            user_email = self.object.email
            
            # Realizar la eliminación
            self.object.delete()
            
            messages.success(
                request, 
                f'Usuario "{user_name}" ({user_email}) eliminado exitosamente.'
            )
            
            # Si es una petición AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Usuario "{user_name}" eliminado exitosamente.',
                    'redirect_url': str(self.success_url)
                })
            
            return redirect(self.success_url)
            
        except Exception as e:
            error_message = f'Error al eliminar el usuario: {str(e)}'
            messages.error(request, error_message)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_message
                })
            
            return redirect(self.success_url)
    
    def post(self, request, *args, **kwargs):
        """Manejar la confirmación de eliminación"""
        return self.delete(request, *args, **kwargs)



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
    
    


