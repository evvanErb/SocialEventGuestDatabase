from django.shortcuts import render, get_object_or_404

from datetime import date

from .models import Guest

def enterGuest(request):
	return render(request, 'entries/enterGuest.html')
	
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
	if(checkForErrors(request) != None):
		return errorPage(request, checkForErrors(request))
	
	blackListedInput = False
	if(request.GET["blackListed"] == 'Yes'):
		blackListedInput = True
		
	if(Guest.objects.filter(firstName=request.GET["firstName"], lastName=request.GET["lastName"]).exists()):
		alreadyThere = "Guest Already Entered"
		
	else:
		alreadyThere = "New guest Created"
		newGuest = Guest.objects.create(firstName = request.GET["firstName"], lastName = request.GET["lastName"], blackListed = blackListedInput, photo = request.GET["photo"], friendsWith = request.GET["friendsWith"], ageWhenEntered = request.GET["ageWhenEntered"], notes = request.GET["notes"], dateEntered = date.today().strftime("%Y-%m-%d"))
		
		newGuest.save()
		
	data = {"alreadyThere":alreadyThere}
	return render(request, 'entries/guestCreated.html', data)
	
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