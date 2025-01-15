from django.db import models
from django.contrib.auth.models import User

# Modèle pour les livres
class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    annee_publication = models.IntegerField()
    exemplaires_disponibles = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.titre} - {self.auteur}"

# Modèle pour les emprunts
class Emprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(null=True, blank=True)
    est_retourne = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.username} a emprunté {self.livre.titre}"

# Modèle pour l'historique des emprunts
class HistoriqueEmprunt(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour = models.DateField()

    def __str__(self):
        return f"Historique: {self.utilisateur.username} - {self.livre.titre}"
