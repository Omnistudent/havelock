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
	
class Question(models.Model):
    name=models.CharField('Question_name',max_length=120,default='question_name')
    
    question_swedish=models.CharField('question_swedish',max_length=1000,default='swedish_question')
    answer1_swedish=models.CharField('answer1_swedish',max_length=1000,default='swedish_answer1')
    answer2_swedish=models.CharField('answer2_swedish',max_length=1000,default='swedish_answer2')
    answer3_swedish=models.CharField('answer3_swedish',max_length=1000,default='swedish_answer3')
    answer4_swedish=models.CharField('answer4_swedish',max_length=1000,default='swedish_answer4')
    
    question_english=models.CharField('question_english',max_length=1000,default='english_question')
    answer1_english=models.CharField('answer1_english',max_length=1000,default='english_answer1')
    answer2_english=models.CharField('answer2_english',max_length=1000,default='english_answer2')
    answer3_english=models.CharField('answer3_english',max_length=1000,default='english_answer3')
    answer4_english=models.CharField('answer4_english',max_length=1000,default='english_answer4')
    correct_answer=models.IntegerField('correct_answer',default=0)

    difficulty=models.FloatField('difficulty',max_length=20,default='0.0')
    area1=models.CharField('area1',max_length=1000,default='general')
    area2=models.CharField('area2',max_length=1000,default='area2')
    area3=models.CharField('area3',max_length=1000,default='area3')



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

	last_active_time = models.DateTimeField(null=True, blank=True)
	name=models.CharField('User Name',max_length=120,default='0')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type=models.CharField('user_type',max_length=120,default='regular')
	x = models.IntegerField("x",default=0)
	y = models.IntegerField("y",default=0)
	xpos = models.IntegerField("xpos",default=0)
	ypos = models.IntegerField("ypos",default=0)
	pending_xpos = models.IntegerField("pending_xpos",default=0)
	pending_ypos = models.IntegerField("pending_ypos",default=0)
	#mapsquare = models.ForeignKey(Mapsquare,on_delete=models.DO_NOTHING)
	mode = models.CharField('mode',max_length=30,blank=True)
	question=models.ForeignKey(Question, blank=True,null=True,on_delete=models.CASCADE)
	correct_answers = models.IntegerField("correct_answers",default=0)
	wrong_answers = models.IntegerField("wrong_answers",default=0)
	temp_label_holder=models.CharField('temp_label_holder',max_length=120,default='x')

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
	map_label=models.CharField('map_label',max_length=120,blank=True)

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


