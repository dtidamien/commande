from django.urls import path

from . import views

app_name = 'commande'
urlpatterns = [
	path('recherche/', views.recherche, name='recherche'),
	path('accueil', views.connexion, name='connexion'),
	path('deconnexion', views.deconnexion, name='deconnexion'),
	path('ajout', views.ajout, name='ajout'),
	path('panier', views.panier, name='panier'),
	path('retirer', views.retirer, name='retirer'),
	path('modifier', views.modifier, name='modifier'),
	path('paiement', views.paiement, name='paiement'),
]