from django.shortcuts import render, get_object_or_404

from datetime import date

from .models import Guest

from .forms import GuestForm

from .functions.functions import handle_uploaded_photo

def enterGuest(request):
	guest = GuestForm()
	return render(request, 'entries/enterGuest.html',{'form':guest})
	
def retrieveGuest(request):
	return render(request, 'entries/retrieveGuest.html')

def retrievingGuest(request):
	if(checkForErrors(request) != None):
			return errorPage(request, checkForErrors(request))
			
	elif(Guest.objects.filter(firstName=request.GET["firstName"], lastName=request.GET["lastName"]).exists()):
		return guestFound(request) 
		
	else:
		return guestNotFound(request)

def guestFound(request):
	theGuest = Guest.objects.get(firstName=request.GET["firstName"], lastName=request.GET["lastName"])
	name = theGuest.__str__()
	
	blackListed = "No guest is Not Black Listed"
	if(theGuest.getBlackListed()):
		blackListed = "YES BLACK LISTED NO ENTRY"
	
	photo = theGuest.getPhoto()
	friendsWith = theGuest.getFriendsWith()
	ageWhenEntered = theGuest.getAgeWhenEntered()
	notes = theGuest.getNotes()
	dateEntered = theGuest.getDateEntered()
	
	guestData = {"name":name, "blackListed":blackListed, "photo":photo, "friendsWith":friendsWith, "ageWhenEntered":ageWhenEntered, "notes":notes, "dateEntered":dateEntered}
	
	return render(request, 'entries/guestFound.html', guestData)

def guestNotFound(request):
	return render(request, 'entries/guestNotFound.html')
	
def guestCreated(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		guest = GuestForm(request.POST, request.FILES)  
		if guest.is_valid():
			handle_uploaded_photo(request.FILES['photo']) 
			 
			firstNameInput = guest.cleaned_data["firstName"]
			lastNameInput = guest.cleaned_data["lastName"]
			blackListedInput = guest.cleaned_data["blackListed"]
			photoInput = guest.cleaned_data["photo"]
			friendsWithInput = guest.cleaned_data["friendsWith"]
			ageWhenEnteredInput = guest.cleaned_data["ageWhenEntered"]
			notesInput = guest.cleaned_data["notes"]
			
			
			if(Guest.objects.filter(firstName=firstNameInput, lastName=lastNameInput).exists()):
				alreadyThere = "Guest Already Entered"
			
			else:
				alreadyThere = "New guest Created"
			
				newGuest = Guest.objects.create(firstName = firstNameInput, lastName = lastNameInput, blackListed = blackListedInput, photo = photoInput, friendsWith = friendsWithInput, ageWhenEntered = ageWhenEnteredInput, notes = notesInput, dateEntered = date.today().strftime("%Y-%m-%d"))
			
				newGuest.save() 
		
			data = {"alreadyThere":alreadyThere}
			return render(request, 'entries/guestCreated.html', data)
			
		else:
				return errorPage(request, checkForErrors(request))
	
	else:
		return errorPage(request, checkForErrors(request))
	
def errorPage(request, errors):
	return render(request, 'entries/errorPage.html', {"errors":errors})
	
def checkForErrors(request):
	errors = []
	for item in request.GET:
		if(request.GET[item] == ""):
			errors.append("[!] Error: " + item + " not inputed")
	
	if(len(errors) != 0):
		return(errors)
	return(None)