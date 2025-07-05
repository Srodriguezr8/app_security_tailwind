from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm, CharField, PasswordInput
from django.core.paginator import Paginator
from django import forms
from django.db.models import Q
from django.views.generic import ListView, UpdateView, DeleteView
import json

from applications.security.components.mixin_crud import ListViewMixin, PermissionMixin, SessionGroupMixin

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
    
    
    
class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'security/users/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'dni', 'direction', 'phone']
    permission_required = 'auth.add_user'
    success_url = reverse_lazy('security:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Usuario'
        context['title1'] = 'Nuevo Usuario'
        context['back_url'] = reverse_lazy('security:user_list')
        return context

    def form_valid(self, form):
        # Crear usuario sin contraseña y inactivo
        user = form.save(commit=False)
        user.username = user.email  # Usar email como username
        user.is_active = False  # Usuario inactivo hasta que active su cuenta
        user.save()
        
        # Enviar email de activación
        self.send_activation_email(user)
        
        messages.success(
            self.request, 
            f'Usuario {user.get_full_name} creado exitosamente. '
            f'Se ha enviado un email de activación a {user.email}'
        )
        return super().form_valid(form)

    def send_activation_email(self, user):
        """Envía email de activación al usuario"""
        current_site = get_current_site(self.request)
        
        # Generar token de activación
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # URL de activación
        activation_url = f"http://{current_site.domain}/security/activate/{uid}/{token}/"
        
        # Contexto para el template del email
        context = {
            'user': user,
            'activation_url': activation_url,
            'site_name': current_site.name,
            'domain': current_site.domain,
        }
        
        # Renderizar template del email
        html_message = render_to_string('security/emails/activation_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Enviar email
        send_mail(
            subject='Activa tu cuenta',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'security/users/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'dni', 'direction', 'phone', 'is_active']
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('security:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['title1'] = 'Modificar Usuario'
        context['back_url'] = reverse_lazy('security:user_list')
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Usuario {form.instance.get_full_name} actualizado exitosamente.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'security/users/user_delete.html'
    permission_required = 'auth.delete_user'
    success_url = reverse_lazy('security:user_list')
    cancel_url = reverse_lazy('security:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuario'
        context['title1'] = 'Confirmar Eliminación'
        context['back_url'] = reverse_lazy('security:user_list')
        return context

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f'Usuario {user.get_full_name} eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


class ActivateAccountView(View):
    """Vista para activar cuenta de usuario"""
    
    def get(self, request, uidb64, token):
        try:
            # Decodificar el ID del usuario
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Verificar si el token es válido
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active:
                # Usuario ya está activo
                messages.info(request, 'Tu cuenta ya está activada. Puedes iniciar sesión.')
                return redirect('login')
            else:
                # Mostrar formulario para crear contraseña
                return render(request, 'security/users/set_password.html', {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'title': 'Activar Cuenta',
                    'title1': 'Crear tu Contraseña'
                })
        else:
            # Token inválido o expirado
            messages.error(request, 'El enlace de activación es inválido o ha expirado.')
            return render(request, 'security/users/activation_invalid.html', {
                'title': 'Enlace Inválido',
                'title1': 'Error de Activación'
            })

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            # Validar contraseñas
            if not password1 or not password2:
                messages.error(request, 'Ambos campos de contraseña son requeridos.')
                return render(request, 'security/users/set_password.html', {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'title': 'Activar Cuenta',
                    'title1': 'Crear tu Contraseña'
                })
            
            if password1 != password2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'security/users/set_password.html', {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'title': 'Activar Cuenta',
                    'title1': 'Crear tu Contraseña'
                })
            
            if len(password1) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return render(request, 'security/users/set_password.html', {
                    'user': user,
                    'uidb64': uidb64,
                    'token': token,
                    'title': 'Activar Cuenta',
                    'title1': 'Crear tu Contraseña'
                })
            
            # Activar usuario y establecer contraseña
            user.set_password(password1)
            user.is_active = True
            user.save()
            
            messages.success(request, '¡Cuenta activada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'El enlace de activación es inválido o ha expirado.')
            return render(request, 'security/users/activation_invalid.html', {
                'title': 'Enlace Inválido',
                'title1': 'Error de Activación'
            })


class RequestNewActivationView(View):
    """Vista para solicitar nuevo enlace de activación"""
    
    def get(self, request):
        return render(request, 'security/users/request_activation.html', {
            'title': 'Solicitar Activación',
            'title1': 'Reenviar Enlace de Activación'
        })
    
    def post(self, request):
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor ingresa tu email.')
            return render(request, 'security/users/request_activation.html', {
                'title': 'Solicitar Activación',
                'title1': 'Reenviar Enlace de Activación'
            })
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_active:
                messages.info(request, 'Tu cuenta ya está activada. Puedes iniciar sesión.')
                return redirect('login')
            
            # Enviar nuevo email de activación
            self.send_activation_email(user, request)
            
            messages.success(
                request, 
                f'Se ha enviado un nuevo enlace de activación a {email}. '
                'Revisa tu bandeja de entrada y spam.'
            )
            
        except User.DoesNotExist:
            # Por seguridad, no revelamos si el email existe o no
            messages.success(
                request, 
                f'Si existe una cuenta con el email {email}, '
                'se ha enviado un enlace de activación.'
            )
        
        return render(request, 'security/users/request_activation.html', {
            'title': 'Solicitar Activación',
            'title1': 'Reenviar Enlace de Activación'
        })
    
    def send_activation_email(self, user, request):
        """Envía email de activación al usuario"""
        current_site = get_current_site(request)
        
        # Generar nuevo token de activación
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # URL de activación
        activation_url = f"http://{current_site.domain}/security/activate/{uid}/{token}/"
        
        # Contexto para el template del email
        context = {
            'user': user,
            'activation_url': activation_url,
            'site_name': current_site.name,
            'domain': current_site.domain,
        }
        
        # Renderizar template del email
        html_message = render_to_string('security/emails/activation_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Enviar email
        send_mail(
            subject='Activa tu cuenta - Nuevo enlace',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )


class UserToggleStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Vista para cambiar estado activo/inactivo del usuario"""
    permission_required = 'auth.change_user'
    
    def post(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            data = json.loads(request.body)
            is_active = data.get('is_active') == '1'
            
            user.is_active = is_active
            user.save()
            
            status_text = "activado" if is_active else "desactivado"
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {user.get_full_name} {status_text} exitosamente.',
                'is_active': user.is_active
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al cambiar estado: {str(e)}'
            })
            
            
            

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