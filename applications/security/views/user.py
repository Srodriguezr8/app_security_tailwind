import json
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import UpdateViewMixin, ListViewMixin, PermissionMixin
from applications.security.forms.user import UserForm, UserStatusForm
from applications.security.models import User
from django.views.generic import ListView, UpdateView
from django.db.models import Q


class UserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/users/list.html'
    model = User
    context_object_name = 'users'
    permission_required = 'view_user'

    def get_queryset(self):
        q = self.request.GET.get("q")
        queryset = super().get_queryset()

        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(dni__icontains=q)
            )

        return queryset.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios'
        context['create_url'] = reverse_lazy('security:user_update', args=[self.request.user.id])  # Ejemplo
        return context


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




