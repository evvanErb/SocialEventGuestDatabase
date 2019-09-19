from django.shortcuts import render, get_object_or_404

from django.utils import timezone
import datetime

from .models import Guest

from .forms import GuestForm

from .functions.functions import handle_uploaded_photo

def enterGuest(request):
	#Pass form to enter guest html page
	guest = GuestForm()
	return render(request, 'entries/enterGuest.html',{'form':guest})
	
def retrieveGuest(request):
	return render(request, 'entries/retrieveGuest.html')

def retrievingGuest(request):
	#Make sure all fields entered
	if(checkForErrors(request) != None):
			return errorPage(request, checkForErrors(request))
			
	#See if guest exists and if so return guest found page with passed request data
	elif(Guest.objects.filter(firstName=request.GET["firstName"], lastName=request.GET["lastName"]).exists()):
		return guestFound(request) 
		
	#See if guest exists and if not then return guest not found page with passed request data
	else:
		return guestNotFound(request)

def guestFound(request):
	#Get the guest and the guest's name
	theGuest = Guest.objects.get(firstName=request.GET["firstName"], lastName=request.GET["lastName"])
	name = theGuest.__str__()
	
	#Set Black Listed to string depeding if the guest black list is True or False
	blackListed = "No guest is Not Black Listed"
	if(theGuest.getBlackListed()):
		blackListed = "YES BLACK LISTED NO ENTRY"
	
	#Get the rest of the guest's info
	photo = theGuest.getPhoto()
	friendsWith = theGuest.getFriendsWith()
	ageWhenEntered = theGuest.getAgeWhenEntered()
	notes = theGuest.getNotes()
	dateEntered = theGuest.getDateEntered()
	
	#Dictionary with guest data
	guestData = {"name":name, "blackListed":blackListed, "photo":photo, "friendsWith":friendsWith, "ageWhenEntered":ageWhenEntered, "notes":notes, "dateEntered":dateEntered}
	
	#Return HTML page with guest data passed to it
	return render(request, 'entries/guestFound.html', guestData)

def guestNotFound(request):
	return render(request, 'entries/guestNotFound.html')
	
def guestCreated(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		
		#Get the entered POST data
		guest = GuestForm(request.POST, request.FILES)  
		#If form valid
		if guest.is_valid():
			#Set new guest data to variables
			firstNameInput = guest.cleaned_data["firstName"]
			lastNameInput = guest.cleaned_data["lastName"]
			blackListedInput = guest.cleaned_data["blackListed"]
			photoInput = guest.cleaned_data["photo"]
			friendsWithInput = guest.cleaned_data["friendsWith"]
			ageWhenEnteredInput = guest.cleaned_data["ageWhenEntered"]
			notesInput = guest.cleaned_data["notes"]
			
			#If the guest's name already exists
			if(Guest.objects.filter(firstName=firstNameInput, lastName=lastNameInput).exists()):
				alreadyThere = "Guest Already Entered"
			
			else:
				alreadyThere = "New guest Created"
				
				#Upload the provided photo
				handle_uploaded_photo(request.FILES['photo']) 
				 
			
				#Create and save new guest
				newGuest = Guest.objects.create(firstName = firstNameInput, lastName = lastNameInput, blackListed = blackListedInput, photo = photoInput, friendsWith = friendsWithInput, ageWhenEntered = ageWhenEnteredInput, notes = notesInput, dateEntered = datetime.datetime.now(tz=timezone.utc))
			
				newGuest.save() 
		
			#Return HTML guest created page with string of whether or not guest already existed
			#or was created
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
	#If item val of form was empty throw an error and return error page
	for item in request.GET:
		if(request.GET[item] == ""):
			errors.append("[!] Error: " + item + " not inputed")
	
	if(len(errors) != 0):
		return(errors)
	return(None)