

def handle_uploaded_photo(p):  
	with open('media/pics/'+p.name, 'wb+') as destination:  
		for chunk in p.chunks():  
			destination.write(chunk)  