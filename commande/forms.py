from django import forms


class ConnexionForm(forms.Form):
	username = forms.CharField(label="nom d'utilisateur", max_length=30)
	password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

	
class RechercheForm(forms.Form):
	saisie = forms.CharField(max_length=100)
	
	def clean_saisie(self):
		saisie = self.cleaned_data['saisie']
		if "vador" in saisie:
			raise forms.ValidationError("Je ne suis pas ton père !")
		return saisie

	
class AjoutForm(forms.Form):
	qt = [(1,"1"),
		  (2,"2"),
		  (3,"3"),
		  (4,"4"),
		  (5,"5"),
		  (6,"6"),
		  (7,"7"),
		  (8,"8"),
		  (9,"9"),
		  (10,"10"),
		  (12,"12"),
		  (20,"20"),
		  (50,"50"),
		  (100,"100"),
		  (200,"200")]
	quantite = forms.ChoiceField(choices=qt, label="Quantité")

