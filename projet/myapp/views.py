from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import LibraryUser, Book, Borrow
from .models import MyUser

# Page d'accueil
def home(request):
    return render(request, 'code.html')

# Inscription
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        

        # Vérification des mots de passe
     

        # Vérifier si l'utilisateur essaie d'utiliser l'email admin
        if email == "admin@gmail.com":
            messages.error(request, "Cet email est réservé à l'administrateur.")
            return redirect('/signup/')

        # Vérifier si l'email existe déjà
        if MyUser.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà enregistré. Veuillez vous connecter.")
            return redirect('/signup/')

        # Créer un nouvel utilisateur
        MyUser.objects.create(email=email, password=password)
        messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
        return redirect('/login/')
    return render(request, "code.html", {"action": "signup"})

# Connexion
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Vérification pour un administrateur automatique
        if email == "admin@gmail.com" and password == "1234":
            user, created = MyUser.objects.get_or_create(email=email)
            user.is_admin = True  # Assurez-vous que l'utilisateur est bien un admin
            user.save()
            # login(request, user)  # Connecte l'administrateur directement
            return render(request,"admin_home.html") 

        # Rechercher l'utilisateur
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            messages.error(request, "Email non enregistré. Veuillez vous inscrire.")
            return redirect('/login/')

        # Vérifier le mot de passe
        if user.password != password:
            messages.error(request, "Email ou mot de passe incorrect.")
            return redirect('/login/')

        # Rediriger selon le rôle
        if user.is_admin:
            return redirect('/admin_dashboard/')
        else:
            return redirect('/user_dashboard/')
    return render(request, "code.html")


# Tableau de bord admin
def admin_dashboard(request):
    return render(request, "admin_home.html")


# Tableau de bord utilisateur simple
def user_dashboard(request):
    return render(request, "user_home.html")

# Déconnexion
def logout_view(request):
    request.session.flush()  # Supprimer toutes les données de session
    return redirect('home')

# Tableau de bord pour l'admin
@login_required
def dashboard(request):
    if not request.session.get('is_admin', False):
        return redirect('books_list')
    books = Book.objects.all()
    return render(request, 'dashboard.html', {'books': books})

# Liste des livres
@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})

# Emprunter un livre
@login_required
def borrow_book(request, book_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(LibraryUser, id=user_id)
    book = get_object_or_404(Book, id=book_id)

    if book.copies_available > 0:
        Borrow.objects.create(user=user, book=book)
        book.copies_available -= 1
        book.save()
        messages.success(request, "Livre emprunté avec succès.")
    else:
        messages.error(request, "Pas d'exemplaires disponibles.")
    return redirect('books_list')

# Retourner un livre
@login_required
def return_book(request, borrow_id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(LibraryUser, id=user_id)
    borrow = get_object_or_404(Borrow, id=borrow_id, user=user)

    if not borrow.return_date:
        borrow.return_date = timezone.now()
        borrow.book.copies_available += 1
        borrow.book.save()
        borrow.save()
        messages.success(request, "Livre retourné avec succès.")
    return redirect('books_list')

