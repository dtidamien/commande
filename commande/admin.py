from django.contrib import admin

from .models import Article, Client, Panier


class ArticleAdmin(admin.ModelAdmin):
	list_display = ('reference', 'designation', 'conditionnement', 'prix_achat', 'prix_vente')# liste des champs à afficher
	# list_filter = ('reference', 'designation', 'prix_achat', 'prix_vente')# liste des filtres
	ordering = ('reference',) # tri par default
	search_fields = ('reference', 'designation') # champs de recherche

admin.site.register(Article, ArticleAdmin)
admin.site.register(Client)
admin.site.register(Panier)