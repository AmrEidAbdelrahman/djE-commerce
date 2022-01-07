from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
		('S','Stripe'),
		('p','PayPal')
	)

class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"1234 Main St"
		}))
	apartment_address = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"Apartment or suite"
		}))
	country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
		'class':'custom-select d-block w-100'
		}))
	zip = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		}))
	same_billing_address = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	save_info = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)