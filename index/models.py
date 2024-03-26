from email.mime import image
from django.db import models

class Contact(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField()
	subject = models.CharField(max_length=2000)
	message = models.TextField()

	def __str__ (self):
		return self.name


class Review(models.Model):
	name = models.CharField(max_length=200)
	image = models.FileField()
	body = models.TextField()

	def __str__ (self):
		return self.name
# Create your models here.