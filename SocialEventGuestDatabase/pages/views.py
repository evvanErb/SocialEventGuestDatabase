from django.shortcuts import render, get_object_or_404

def homePage(request):
	return render(request, 'pages/homePage.html')
	
def passwordPreEnterGuest(request):
	return render(request, 'pages/passwordPreEnterGuest.html')
	