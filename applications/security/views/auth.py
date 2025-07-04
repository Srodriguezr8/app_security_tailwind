
import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from applications.security.models import User

User = get_user_model()

# ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("security:signin")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    if request.method == "GET":
        return render(request, "security/auth/signin.html", {
            "title": "Login",
            "title1": "Inicio de Sesión"
        })

    elif request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        print("Datos recibidos:", username, password)

        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Correo y contraseña son obligatorios'
            }, status=400)

        try:
            user_server = User.objects.get(email=username)
            print('user_server_name: ', user_server.email)
            user = authenticate(request, username=user_server.email, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'redirect_url': reverse("security:home")
            })
        else:
            print(f"No se pudo autenticar al usuario '{username}'")
            return JsonResponse({
                'success': False,
                'error': 'Correo electrónico o contraseña incorrectos.'
            }, status=400)



      