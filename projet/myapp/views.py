from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Page principale après connexion
        else:
            messages.error(request, 'Email ou mot de passe invalide.')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        # Vérifie si l'utilisateur existe déjà
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Cet email est déjà utilisé.')
        else:
            User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Compte créé avec succès.')
            return redirect('login')  # Redirige vers la page de connexion
    return render(request, 'login.html')