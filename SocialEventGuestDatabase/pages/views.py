from django.shortcuts import render, get_object_or_404

from entries.views import enterGuest

def homePage(request):
	return render(request, 'pages/homePage.html')
	
def passwordPreEnterGuest(request):
	wrongPass = {"wrongPass":False}
	if("enterGuestPassword" in request.GET.keys()):
		#If password correct to hard coded pass then call enter guest view
		if(request.GET["enterGuestPassword"] == "PASSWORD"):
			return enterGuest(request)
		#else return password page but with wrong pass true so text displays
		else:
			wrongPass["wrongPass"] = True
	
	return render(request, 'pages/passwordPreEnterGuest.html', wrongPass)
	