from django.db import models
from django.contrib.auth.models import User




#class UserXc(AbstractUser):
  #  x = models.IntegerField(null=True, blank=True)
  #  y = models.IntegerField(null=True, blank=True)

class Venue(models.Model):
	name=models.CharField('Venue Name',max_length=120)
	adress=models.CharField('Adress',max_length=120)
	zip_code=models.CharField('Zip Code',max_length=120)
	phone=models.CharField('Contact Phone',max_length=120)
	description=models.TextField(blank=True)

	def __str__(self):
		return self.name


class Environment(models.Model):
	name=models.CharField('Square Name',max_length=120)
	x=models.CharField('X',max_length=120)
	y=models.CharField('Y',max_length=120)
	z=models.CharField('Z',max_length=120)
	description=models.TextField(blank=True)

	def __str__(self):
		return self.name

class MyPlayer(models.Model):
	name=models.CharField('Square Name',max_length=120)
	x=models.CharField('X',max_length=120)
	y=models.CharField('Y',max_length=120)
	z=models.CharField('Z',max_length=120)
	description=models.TextField(blank=True)
	environment=models.ForeignKey(Environment, blank=True,null=True,on_delete=models.CASCADE)
	email=models.EmailField('User Email')

	def __str__(self):
		return self.name
	
class UserProfile(models.Model):
	name=models.CharField('User Name',max_length=120,default='0')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	x = models.IntegerField("x",default=0)
	y = models.IntegerField("y",default=0)
	xpos = models.IntegerField("xpos",default=0)
	ypos = models.IntegerField("ypos",default=0)
	#mapsquare = models.ForeignKey(Mapsquare,on_delete=models.DO_NOTHING)
	mode = models.CharField('mode',max_length=30,blank=True)
	def __str__(self):
		return str(self.user)
	
class UserProfile2(models.Model):
	name=models.CharField('User Name',max_length=120,default='0')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	x = models.IntegerField("x",default=0)
	y = models.IntegerField("y",default=0)
	xpos = models.IntegerField("xpos",default=0)
	ypos = models.IntegerField("ypos",default=0)
	def __str__(self):
		return str(self.name)









class Square(models.Model):
	name=models.CharField('Square Name',max_length=120)
	x=models.CharField('X',max_length=120)
	y=models.CharField('Y',max_length=120)
	z=models.CharField('Z',max_length=120)
	description=models.TextField(blank=True)
	environment=models.ForeignKey(Environment, blank=True,null=True,on_delete=models.CASCADE)
	occupants=models.ManyToManyField(MyPlayer,blank=True)
	
	#occupants3 is used most
	occupants3 = models.ManyToManyField(UserProfile, blank=True, default=[])
	occupants4 = models.ManyToManyField(UserProfile2, blank=True, default=[])

	image = models.CharField(max_length=100,default='null.png')
	original_image=models.CharField(max_length=100,default='null.png')
	#image = models.CharField(max_length=100, default='null.png')
	territory = models.TextField(blank=True)

	def __str__(self):
		return self.name






class MyClubUser(models.Model):
	first_name=models.CharField('First Name',max_length=120)
	last_name=models.CharField('Last Name',max_length=120)
	y=models.CharField('Y',max_length=120)
	z=models.CharField('Z',max_length=120)
	description=models.TextField(blank=True)
	environment=models.ForeignKey(Environment, blank=True,null=True,on_delete=models.CASCADE)
	email=models.EmailField('User Email')

	def __str__(self):
		return self.first_name+' '+self.last_name

class Event(models.Model):
    name=models.CharField('Event Name',max_length=120)
    event_date=models.DateTimeField('Event Date')
    avenue=models.CharField('Avenue',max_length=120)
    manager=models.CharField('Manager',max_length=120)
    description=models.TextField(blank=True)
    attendees=models.ManyToManyField(MyClubUser,blank=True)

    def __str__(self):
	    return self.name

