from django.urls import path

from applications.security.views.auth import signin, signout
from applications.security.views.group import GroupCreateView, GroupDeleteView, GroupListView, GroupUpdateView
from applications.security.views.group_module_pemission import DeleteGroupModulePermissionView, GroupModulePermissionListView,GroupModulePermissionPermissionsView,PemissionsModuleView, SaveGroupModulePermissionView
from applications.security.views.home import ModuloTemplateView, StartTemplateView, get_group_menus, test_group_menus
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.user import UserListView, UserUpdateView, UserUpdateView,toggle_user_status, user_list_view


app_name='security' # define un espacio de nombre para la aplicacion
urlpatterns = [
    
  path('home/', ModuloTemplateView.as_view(), name='home'),
  path('', StartTemplateView.as_view()),

  # rutas de modulos
  path('module_list/',ModuleListView.as_view() ,name="module_list"),
  path('module_create/', ModuleCreateView.as_view(),name="module_create"),
  path('module_update/<int:pk>/', ModuleUpdateView.as_view(),name='module_update'),
  path('module_delete/<int:pk>/', ModuleDeleteView.as_view(),name='module_delete'),

# rutas de menus
  path('menu_list/',MenuListView.as_view() ,name="menu_list"),
  path('menu_create/', MenuCreateView.as_view(),name="menu_create"),
  path('menu_update/<int:pk>/', MenuUpdateView.as_view(),name='menu_update'),
  path('menu_delete/<int:pk>/', MenuDeleteView.as_view(),name='menu_delete'),
  

    # Rutas de usuarios user_list
    path('user_list/', UserListView.as_view(), name="user_list"),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:user_id>/toggle-status/', toggle_user_status, name='user_toggle_status'),

 
  path('group_list/',GroupListView.as_view() ,name="group_list"),
  path('group_create/', GroupCreateView.as_view(),name="group_create"),
  path('group_update/<int:pk>/', GroupUpdateView.as_view(),name='group_update'),
  path('group_delete/<int:pk>/', GroupDeleteView.as_view(),name='group_delete'),

  # rutas de group  module permission
  path('group_module_permission_list/',GroupModulePermissionListView.as_view() ,name="group_module_permission_list"),
  path('group-module-permission/permissions/', GroupModulePermissionPermissionsView.as_view(), name='group_module_permissions_by_group_module'),
  path('module/<int:pk>/permissions/', PemissionsModuleView.as_view(), name='module_permissions'),
  path('group-module-permission/save/', SaveGroupModulePermissionView.as_view(), name='save_group_module_permission'),
  path('group-module-permission/delete/', DeleteGroupModulePermissionView.as_view(), name='delete_group_module_permission'),


  # list menus by grupos
  path('get_group_menus/', get_group_menus, name='get_group_menus'),

  
   # rutas de autenticacion
  path('logout/', signout, name='signout'),
  path('signin/', signin, name='signin'),
  
]