from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)# le contact est un user ou vide
	nom_societe = models.CharField(max_length=20)
	
	def __str__(self):# renvoi le nom de la societe
		return self.nom_societe

	
class Article(models.Model):
	reference = models.CharField(max_length=20)
	designation = models.CharField(max_length=40)
	conditionnement = models.IntegerField()
	prix_achat = models.DecimalField(max_digits=11,decimal_places=2) # en centimes max 9M euros
	prix_vente = models.DecimalField(max_digits=11,decimal_places=2) # en centimes max 9M euros
	
	def __str__(self):# renvoi la designation en intitulé
		return self.designation
	
	def Pa(self):# en euros
		return self.prix_achat / 100
	def Pv(self):# en euros
		return self.prix_vente / 100

	
class Panier(models.Model):
	article = models.ForeignKey(Article, on_delete=models.CASCADE)# si l'article est supprimé on supprime ses paniers
	client = models.ForeignKey(Client, on_delete=models.CASCADE) # si le client est supprimé on supprime ses paniers
	date = models.DateTimeField(default=timezone.now)
	quantite = models.IntegerField()
	tarif = models.DecimalField(max_digits=11,decimal_places=2) # en centime
	
	def prix(self):# en euros
		return self.tarif / 100
	
	def prix_unitaire(self):# pour un article de la ligne en euros
		return (self.tarif / self.quantite) / 100
	