from django import forms  

class GuestForm(forms.Form):  		
	firstName = forms.CharField(label="Enter First Name:",max_length = 25)  
	lastName  = forms.CharField(label="Enter Last Name:", max_length = 25)  
	blackListed = forms.BooleanField(required = False, label="Black Listed?")
	photo = forms.ImageField(label="Choose Photo:")
	friendsWith = forms.CharField(max_length = 250, label="Friends with / Knows:")
	ageWhenEntered = forms.IntegerField(label="Age:")
	notes = forms.CharField(label="Notes:")