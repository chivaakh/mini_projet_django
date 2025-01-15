from django.db import models

# Modèle pour les utilisateurs de la bibliothèque
class LibraryUser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  

# Modèle pour les livres
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    publication_year = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"  

    def borrow_book(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            self.save()
        else:
            raise ValueError("No copies available")

    def return_book(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.save()
        else:
            raise ValueError("All copies are already returned")

# Modèle pour les emprunts
class Borrow(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"

    def mark_as_returned(self):
        if not self.is_returned:
            self.is_returned = True
            self.return_date = models.DateTimeField(auto_now=True)
            self.book.return_book()
            self.save()
        else:
            raise ValueError("This book has already been returned")
