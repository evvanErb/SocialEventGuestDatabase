from django.db import models

class Guest(models.Model):
	firstName = models.CharField(max_length = 25)
	lastName = models.CharField(max_length = 25)
	blackListed = models.BooleanField(default=False)
	photo = models.ImageField(upload_to='pics/')
	friendsWith = models.CharField(max_length = 250)
	ageWhenEntered = models.IntegerField()
	notes = models.TextField()
	dateEntered = models.DateTimeField()
	
	def __str__(self):
		return (self.firstName + " " + self.lastName)
	
	def getBlackListed(self):
		return self.blackListed
		
	def getPhoto(self):
		return self.photo
		
	def getFriendsWith(self):
		return self.friendsWith
		
	def getAgeWhenEntered(self):
		return self.ageWhenEntered
	
	def getNotes(self):
		return self.notes
		
	def getDateEntered(self):
		return self.dateEntered.strftime('%b %e %Y')