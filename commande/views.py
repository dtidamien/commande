from django.shortcuts import render, redirect
from django.db.models import Q, Count, OuterRef, Subquery, Sum
# OU ET, comptage, getion de sous requetes, somme
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import * # pour convertir en decimal

from .models import Article, Panier, Client
from .forms import RechercheForm, AjoutForm, ConnexionForm


def recherche(request):
	if request.method == "GET":
		recherche = RechercheForm(request.GET)
		if recherche.is_valid():
			saisie = recherche.cleaned_data['saisie']
			envoi = True
			quantite = AjoutForm()
			if request.GET['saisie'] == '*':
				liste_articles = Article.objects.all()
			else:
				liste_articles = Article.objects.filter(Q(designation__contains=request.GET['saisie']) | Q(reference__contains=request.GET['saisie']))
				# select * from article where designation like 'saisie' OR reference like 'saisie'
		else:
			recherche = RechercheForm()
	else:
		recherche = RechercheForm()
	if request.user.is_authenticated:
		client = Client.objects.get(user_id = request.user.id)# recuperation de l'id du client à partir de l'user identifié
		sous_total = Panier.objects.filter(client_id = client.id).aggregate(nb=Sum('quantite'))
		# comptage du nombre de panier (articles) pour le client
	return render(request, 'recherche.html', locals())


def connexion(request):
	error = False
	if request.method == "POST":
		form = ConnexionForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect(reverse('commande:recherche'))# on va en vue recherche apres la connexion
			else:
				error = True
	else:
		form = ConnexionForm()
	return render(request, 'accueil.html', locals())
	

def deconnexion(request):
	logout(request)
	return redirect(reverse('commande:connexion'))


def ajout(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			ajout = AjoutForm(request.POST)
			if ajout.is_valid():
				article = request.POST['article']
				quantite = ajout.cleaned_data['quantite']
				client = Client.objects.get(user_id = request.user.id)
				# recuperation de l'id du client à partir de l'user identifié
				
				try:
					article_existant = Panier.objects.get(article_id=article,client_id=client.id)
					# on cherche l'article dans le panier
					article_existant.quantite += int(quantite)
					article_existant.save()
				
				except:# si il n'existe pas on l'ajoute
					tarif = request.POST['prix']
					tarif = Decimal(tarif.replace(',','.')) # conversion d'une chaine en decimale pour le prix (en centimes)
					panier = Panier.objects.create(date=timezone.now(),quantite=quantite,article_id=article,client_id=client.id,tarif=tarif*int(quantite))
									
				saisie = request.POST['saisie']
	return redirect(reverse('commande:recherche')+"?saisie="+saisie)# on renvoi la saisie en get

		
def panier(request):
	if request.user.is_authenticated:
		client = Client.objects.get(user_id = request.user.id)
		# recuperation de l'id du client à partir de l'user identifié
		
		q1 = Article.objects.filter(panier=OuterRef("pk"))
		# selection des liaisons pour la sous requete
		
		le_panier = Panier.objects.filter(client_id = client.id).annotate(reference=Subquery(q1.values('reference')), designation=Subquery(q1.values('designation')), conditionnement=Subquery(q1.values('conditionnement')))
		# panier du client + annotation de la sous-requete
		
		sous_total = le_panier.aggregate(st=Sum('tarif'), nb=Sum('quantite'))
		# on fait la somme des prix*quantité en centimes pour tout le panier et on compte le nb d'article
		
		try:
			sous_total_euros = (sous_total['st']/100).quantize(Decimal('.01'), rounding=ROUND_DOWN)
			# formatage du resultat en euros arondis
		except:
			sous_total_euros = 0
		
	return render(request, 'panier.html', locals())


def retirer(request):
	if request.method == "POST":
		article = request.POST['article']
		client = Client.objects.get(user_id = request.user.id)
		# recuperation de l'id du client à partir de l'user identifié
		
		article_del = Panier.objects.get(article_id=article,client_id=client.id)
		# selection de l'article à supprimer
		article_del.delete()
	return redirect(reverse('commande:panier'))
	

def modifier(request):
	if request.method == "POST":
		article = Article.objects.get(pk = request.POST['article'])
		# recuperation de l'article
		
		quantite = request.POST['quantite']
		client = Client.objects.get(user_id = request.user.id)
		# recuperation de l'id du client à partir de l'user identifié
		
		article_modif = Panier.objects.get(article_id=article.id,client_id=client.id)
		# selection de l'article à modifier dans le panier
		article_modif.quantite = int(quantite)
		article_modif.tarif = int(quantite)*article.prix_vente
		article_modif.save()
		
	return redirect(reverse('commande:panier'))


def paiement(request):
	return render(request, 'paiement.html')

	