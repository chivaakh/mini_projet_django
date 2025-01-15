from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class MyUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)  # True pour l'administrateur, False pour un utilisateur simple

    def __str__(self):
        return self.email

# Modèle pour les utilisateurs
class LibraryUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Assurez-vous de sécuriser les mots de passe (hashing)
    is_admin = models.BooleanField(default=False)  # Pour différencier admin et utilisateur simple

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({'Admin' if self.is_admin else 'User'})"

# Modèle pour les livres
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    copies_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

# Modèle pour les emprunts
class Borrow(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"

    def is_returned(self):
        return self.return_date is not None
