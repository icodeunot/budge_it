# Importing required libraries
from django import forms


# Creating a form class for the expense
class ExpenseForm(forms.Form):
	
	# Defining the fields for the form
	title = forms.CharField()
	amount = forms.IntegerField()
	category = forms.CharField()
	
	# Defining the widgets for the form
	widget = {
		'title': forms.TextInput(attrs={'class': 'input-group form-control form-control-lg'}),
		'amount': forms.TextInput(attrs={'class': 'input--group form-control form-control-lg'}),
	}
