from django import forms

class searchForm(forms.Form):
	search_term = forms.CharField(
		label = 'search_term',
		widget = forms.TextInput(attrs={'placeholder': 'Enter name of the product'})
	)