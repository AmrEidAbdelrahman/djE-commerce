from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
		('S','Stripe'),
		('p','PayPal')
	)

class CheckoutForm(forms.Form):
	billing_address1 = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"1234 Main St"
		}))
	billing_address2 = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"Apartment or suite"
		}))
	billing_country = CountryField(blank=True,blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
		'class':'custom-select d-block w-100'
		}))
	billing_zip = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		}))
	shipping_as_billing = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	set_default_billing = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	use_default_billing = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	# ===========================================================
	# ===========================================================
	shipping_address1 = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"1234 Main St"
		}))
	shipping_address2 = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':"Apartment or suite"
		}))
	shipping_country = CountryField(blank=True,blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
		'class':'custom-select d-block w-100'
		}))
	shipping_zip = forms.CharField(required=False ,widget=forms.TextInput(attrs={
		'class':'form-control',
		}))
	set_default_shipping = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))
	use_default_shipping = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
		'class':'form-check-input'
		}))

	# ============================================================
	payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class RefundForm(forms.Form):
	ref_code = forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control',
		'placeholder':""
		}))
	description = forms.CharField(widget=forms.Textarea(attrs={
		'class':'form-control',
		}))