from django.db import models
from django.contrib.auth.models import User


class Usertbl(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	contact = models.CharField(max_length=20,null=True)
	gender = models.CharField(max_length=10)
	image = models.FileField(upload_to='users',null=True)

	def __str__(self):
		return self.user.first_name+" "+self.user.last_name


class Blogtbl(models.Model):
	user = models.ForeignKey(Usertbl,on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	introduction = models.CharField(max_length=300,null=True)
	description = models.TextField()
	created_date = models.DateField()
	image = models.FileField(upload_to='blogs',null=True)
	status = models.CharField(max_length=20)

	def __str__(self):
		return self.title
	

class Contacttbl(models.Model):
	sender_name = models.CharField(max_length=200,null=True)
	sender_email = models.EmailField()
	sender_message = models.TextField()

	def __str__(self):
		return self.sender_name