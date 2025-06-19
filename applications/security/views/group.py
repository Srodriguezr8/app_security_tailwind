
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.db.models import Q

from applications.security.forms.group import GroupForm


class GroupListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'security/group/list.html'
    model = Group
    context_object_name = 'group'
    permission_required = 'view_group'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.OR)
            self.query.add(Q(permissions__name__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('security:group_create')
        return context


class GroupCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Group
    template_name = 'security/group/form.html'
    form_class = GroupForm
    success_url = reverse_lazy('security:group_list')
    permission_required = 'add_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Grupo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        messages.success(self.request, f"Éxito al crear al grupo {group.name}")
        return response


class GroupUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Group
    template_name = 'security/group/form.html'
    form_class = GroupForm
    success_url = reverse_lazy('security:group_list')
    permission_required = 'change_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Grupo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        messages.success(self.request, f"Éxito al actualizar los permisos del grupo sobre el módulo' {group.name}.")
        return response


class GroupDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Group
    template_name = 'core/delete.html'
    success_url = reverse_lazy('security:group_list')
    permission_required = 'delete_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Grupo'
        context['description'] = f"¿Desea eliminar el grupo: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        group_name = self.object.name
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el grupo {group_name}.")
        
        return response
    
class GroupPermissionsView(View):
    def get(self, request, pk):
        try:
            group = Group.objects.get(pk=pk)
            permissions = list(group.permissions.values('name'))
            return JsonResponse({'permissions': permissions})
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Grupo no encontrado'}, status=404)
        
class GroupPermissionsDetailView(DetailView):
    model = Group  # Muy importante definir el modelo

    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()  # Usará pk de kwargs automáticamente
            permissions = list(obj.permissions.values('name'))
            return JsonResponse({'permissions': permissions})
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Grupo no encontrado'}, status=404)