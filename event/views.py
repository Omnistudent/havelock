from django.shortcuts import render,redirect
from django.contrib.auth.models import User
#import calendar
#from calendar import HTMLCalendar
#from datetime import datetime
#from .models import Event
from .models import Square
#from .models import MyPlayer
from .models import UserProfile
from .models import Question
import random
from random import shuffle
#from django.http import HttpResponse
#from django.http import JsonResponse
#import json
import math
from django.contrib.auth import authenticate, login
import string
#from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.conf import settings
import os

import csv
#from django.http import HttpResponse


def moveallowed(startx,endx,starty,endy):
    
    p1=[int(startx),int(starty)]
    p2=[int(endx),int(endy)]
    pdist=math.dist(p1,p2)
    
    if pdist<1.5:
        endsquare = Square.objects.get(x=endx, y=endy)
        if endsquare.image=='land.png':
            return False
        return True
    return False


def help(request):
    return render(request,'event/help.html',
        {})

def home(request):
    if not request.user.is_authenticated:

            # Generate a random username and password
        username10 = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        # Create a new user with the generated username and password
        user = User.objects.create_user(username=username10, password=password)
        question = Question.objects.filter(name='Correct_1').order_by('?').first()
        user_profile = UserProfile.objects.create(user=user,name=user,x='0',y='0',xpos=5,ypos=5,pending_xpos=0,pending_ypos=0,correct_answers=0,wrong_answers=0,question=question,user_type='temp',mode='move')
        user.userprofile=user_profile

        # Authenticate and log in the user
        user = authenticate(request, username=username10, password=password)

        # Set square to be occupied by user
        beginsquare = Square.objects.get(x=5, y=5)
        beginsquare.occupants3.add(user.userprofile)
        beginsquare.save()
        login(request, user)

    user=request.user
    grid_size_x = 15
    grid_size_y = 15

    myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
    myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)

    startx = int(user.userprofile.x)
    stopx = int(user.userprofile.x)+grid_size_x
    starty = int(user.userprofile.y)
    stopy = int(user.userprofile.y)+grid_size_y

    charsx = [str(i) for i in range(startx, stopx)]
    charsy = [str(i) for i in range(starty, stopy)]

    try:
        question = user.userprofile.question
    except:
        question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()

    answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]

    if request.method == 'POST':
        sent_action = request.POST.get('command')
        sent_answer = request.POST.get('answer')
        if sent_action == 'answer':
            right_answer=user.userprofile.question.answer1_swedish
            ############################
            # Correct answer
            ############################
            if right_answer == sent_answer:

                # increment right answers
                user.userprofile.correct_answers+=1

                # delete from starting square
                startsquare = Square.objects.get(y=str(user.userprofile.ypos),x=str(user.userprofile.xpos))
                startsquare.occupants3.remove(user.userprofile)
                startsquare.save()

                # add userprofile to end square
                endsquare = Square.objects.get(x=user.userprofile.pending_xpos, y=user.userprofile.pending_ypos)
                endsquare.occupants3.add(user.userprofile)
                endsquare.save()
                
                # get moved direction
                movedx,movedy=getmovedir(user.userprofile.xpos,user.userprofile.ypos,user.userprofile.pending_xpos,user.userprofile.pending_ypos)

                # set new userprofile coordinates
                user.userprofile.xpos=user.userprofile.pending_xpos
                user.userprofile.ypos=user.userprofile.pending_ypos
                user.userprofile.pending_xpos=0
                user.userprofile.pending_ypos=0
                user.userprofile.save()

                # adjust view
                
                if movedx==1:
                    temp=user.userprofile.x
                    user.userprofile.x=temp+1
                    user.userprofile.save()
                   
                if movedx==-1:
                    temp=user.userprofile.x
                    user.userprofile.x=temp-1
                    user.userprofile.save()
                if movedy==-1:
                    temp=user.userprofile.y
                    user.userprofile.y=temp-1
                    user.userprofile.save()
                if movedy==1:
                    temp=user.userprofile.y
                    user.userprofile.y=temp+1
                    user.userprofile.save()

                myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
                
                #set question to correct
                question = Question.objects.filter(name='Correct_1').order_by('?').first()
                user.userprofile.question=question
                user.userprofile.save()
                # there shouldnt be any answers

                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                overlays=getLabels(user,dbsquares,30)
                return render(request,'event/home.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
            # end of right answer
            else: #wrong answer
                print('wrog')
                user.userprofile.wrong_answers+=1
                user.userprofile.save()
                myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)

                question = Question.objects.filter(name='Wrong_1').order_by('?').first()
                user.userprofile.question=question
                user.userprofile.save()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                overlays=getLabels(user,dbsquares,30)
                return render(request,'event/home.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})

            # end of wrong answer
        # end of command: answer

        # command wasnt answer, so use wants to move

        try:
            sent_x = request.POST.get('sent_x')
            print('sent x'+sent_x)
        except:
            print('could not get x')

        try:
            sent_y = request.POST.get('sent_y')
        except:
            print('could not get y')

        # User wants to move, create a question
        if user.userprofile.mode=="move":
            
            #load_questions_from_file()
            #export_questions_to_csv()
            if moveallowed(user.userprofile.xpos,sent_x,user.userprofile.ypos,sent_y):


                user.userprofile.pending_xpos=sent_x
                user.userprofile.pending_ypos=sent_y
                
                endsquare = Square.objects.get(y=str(user.userprofile.pending_ypos),x=str(user.userprofile.pending_xpos))

                if endsquare.question_area1:
                    question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3, area3=endsquare.question_area1).order_by('?').first()
                else:
                    question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()


                user.userprofile.question=question
                user.userprofile.save()
                #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

                myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)

                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                shuffle(answers)  # shuffles the answers randomly
                user.userprofile.question=question
                user.userprofile.save()
            # end of if moveallowed
        # end of if mode move

        # Send ranges,database,question and randomly ordered answers
        myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
        overlays=getLabels(user,dbsquares,30)
        return render(request,'event/home.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
    # end of if request was post


    else: # if request method was not post

        dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

        # Send ranges,database,question and randomly ordered answers
        overlays=getLabels(user,dbsquares,30)
        return render(request,'event/home.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})





def getmovedir(xstart,ystart,xend,yend):
    dx=int(int(xend)-int(xstart))
    dy=int(yend-ystart)
    return (dx,dy)

def delete_inactive_temp_users():
    threshold = timezone.now() - timedelta(minutes=10)
    inactive_users = User.objects.filter(userprofile__user_type='temp', userprofile__last_active_time__lt=threshold)
    inactive_users.delete()

def getDatabaseAndView(userx,usery,gridx,gridy):
    myrange_x=range(userx,int(userx)+gridx)
    myrange_y=range(usery,int(usery)+gridy)

    startx = int(userx)
    stopx = int(userx)+gridx
    starty = int(usery)
    stopy = int(usery)+gridy

    charsx = [str(i) for i in range(startx, stopx)]
    charsy = [str(i) for i in range(starty, stopy)]
    dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

    return (myrange_x,myrange_y,dbsquares)

def getLabels(user,gottendata,squaresize):


    #testsquare=Square.objects.filter(x='5',y='5').first()
    #testsquare.map_label="Start"
    #testsquare.save()

    #testsquare2=Square.objects.filter(x='10',y='5').first()
    #testsquare2.map_label="Vardagens Hav"
    #testsquare2.save()


    labeled_squares = gottendata.exclude(Q(map_label__isnull=True) | Q(map_label__exact='')).all()
    returnArray=[]
    static_images_path = os.path.join(settings.STATICFILES_DIRS[0], 'event/images')
    print(static_images_path)
    for lab in labeled_squares:
        image_location=os.path.join(static_images_path, lab.map_label)
        try:
            width, height = get_image_size(image_location)
            print(f'The image size is {width}x{height} pixels.')
        except:
            print(image_location)
            width=0
            height=0
        xcoord=int(lab.x)-int(user.userprofile.x)
        ycoord=int(lab.y)-int(user.userprofile.y)
        xPixels=(xcoord*squaresize)-squaresize*2
        yPixels=ycoord*squaresize-squaresize*2
        print('xpixels:'+str(xPixels))
        returnArray.append([lab.map_label,yPixels,xPixels])
        print(lab.map_label)

    return returnArray

def editmap(request):
    user=request.user
    grid_size_x = 21
    grid_size_y = 21

    myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
    myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)

    startx = int(user.userprofile.x)
    stopx = int(user.userprofile.x)+grid_size_x
    starty = int(user.userprofile.y)
    stopy = int(user.userprofile.y)+grid_size_y

    charsx = [str(i) for i in range(startx, stopx)]
    charsy = [str(i) for i in range(starty, stopy)]

    try:
        question = user.userprofile.question
    except:
        question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()

    answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]

    if request.method == 'POST':
        sent_action = request.POST.get('command')
        sent_answer = request.POST.get('answer')
        
        print("sent_action was:"+sent_action)
        if sent_action == 'move_view':
            sent_x = request.POST.get('sent_x')
            sent_y = request.POST.get('sent_y')
            temp=user.userprofile.x
            user.userprofile.x=temp+int(sent_x)
            temp=user.userprofile.y
            user.userprofile.y=temp+int(sent_y)
            user.userprofile.save()

            myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
            overlays=getLabels(user,dbsquares,30)
            return render(request,'event/editmap.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
        # end of command: move_view
        if sent_action == 'change_mode':
            sent_mode = request.POST.get('newmode')
            try:
                label_text= request.POST.get('label_text')
                print('labeltest'+label_text)
            except:
                print('could not get label text')
            question_text= request.POST.get('question_text')
            user.userprofile.mode=sent_mode
            user.userprofile.temp_label_holder=label_text
            user.userprofile.save()
            myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
            overlays=getLabels(user,dbsquares,30)
            label_text= request.POST.get('label_text')
            print('heres the label text'+label_text)
            return render(request,'event/editmap.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})



        # command wasnt answer, so use wants to move

        try:
            sent_x = request.POST.get('sent_x')
            print('sent x'+sent_x)
        except:
            print('could not get x')

        try:
            sent_y = request.POST.get('sent_y')
        except:
            print('could not get y')

        # User wants to move, create a question
        if user.userprofile.mode=="move":
            if moveallowed(user.userprofile.xpos,sent_x,user.userprofile.ypos,sent_y):
                question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()
                user.userprofile.pending_xpos=sent_x
                user.userprofile.pending_ypos=sent_y
                user.userprofile.question=question
                user.userprofile.save()
                #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

                myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)



                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                shuffle(answers)  # shuffles the answers randomly
                user.userprofile.question=question
                user.userprofile.save()
            # end of if moveallowed
        # end of if mode move

        # User wants to paint sea
        if user.userprofile.mode=="paint sea":
            try:
                square = Square.objects.get(x=sent_x, y=sent_y)
            except Square.DoesNotExist:
                square = Square.objects.create(x=sent_x, y=sent_y, name='sea3', image='sea.png',)

        if user.userprofile.mode=="paint land":
            try:
                square = Square.objects.get(x=sent_x, y=sent_y)
            except Square.DoesNotExist:
                square = Square.objects.create(x=sent_x, y=sent_y, name='land', image='land.png',)
        if user.userprofile.mode=="delete":
            try:
                square = Square.objects.get(x=sent_x, y=sent_y)
                square.delete()
            except Square.DoesNotExist:
                print('no square at there')
        if user.userprofile.mode=="addlabel":
            try:
                square = Square.objects.get(x=sent_x, y=sent_y)
            except Square.DoesNotExist:
                print('no square at there')
                    #testsquare2=Square.objects.filter(x='10',y='5').first()
            square.map_label=user.userprofile.temp_label_holder
            square.save()

        if user.userprofile.mode=='questionarea1':
            try:
                square = Square.objects.get(x=sent_x, y=sent_y)
                print('set q in area:'+str(sent_x)+'gg'+str(sent_y))
                square.question_area1=user.userprofile.temp_label_holder
                square.save()
            except Square.DoesNotExist:
                print('no square at there')


              
            
        # end of if paint sea

        # Send ranges,database,question and randomly ordered answers
        myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
        overlays=getLabels(user,dbsquares,30)
        return render(request,'event/editmap.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
    # end of if request was post


    else: # if request method was not post

        dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

        # Send ranges,database,question and randomly ordered answers
        overlays=getLabels(user,dbsquares,30)

        
        return render(request,'event/editmap.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})

def get_image_size(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
    return width, height

def export_questions_to_csv():
    with open("test.csv", mode='w', encoding='UTF-16', newline='') as csv_file:


        #fieldnames = ['id', 'name','question_swedish','answer1_swedish','answer2_swedish','answer3_swedish','answer4_swedish', 'question_english','answer1_english','answer2_english','answer3_english','answer4_english','area1', 'area2', 'area3','difficulty']
        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer = csv.DictWriter(csv_file, fieldnames=['id', 'name', 'question_swedish', 'answer1_swedish', 'answer2_swedish', 'answer3_swedish', 'answer4_swedish', 'question_english', 'answer1_english', 'answer2_english', 'answer3_english', 'answer4_english', 'area1', 'area2', 'area3', 'difficulty'], delimiter='\t')
        writer.writeheader()

        for question in Question.objects.all():
            writer.writerow({
                'id': question.id,
                'name': question.name,
                'question_swedish': question.question_swedish,
                'answer1_swedish': question.answer1_swedish,
                'answer2_swedish': question.answer2_swedish,
                'answer3_swedish': question.answer3_swedish,
                'answer4_swedish': question.answer4_swedish,
                'question_english': question.question_english,
                'answer1_english': question.answer1_english,
                'answer2_english': question.answer2_english,
                'answer3_english': question.answer3_english,
                'answer4_english': question.answer4_english,
                'area1': question.area1,
                'area2': question.area2,
                'area3': question.area3,
                'difficulty': question.difficulty,
            })

   
    print('wrote file')


def load_questions_from_file():
    with open(f"test.csv", mode='r', encoding='UTF-16', newline='') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=['id', 'name', 'question_swedish', 'answer1_swedish', 'answer2_swedish', 'answer3_swedish', 'answer4_swedish', 'question_english', 'answer1_english', 'answer2_english', 'answer3_english', 'answer4_english', 'area1', 'area2', 'area3', 'difficulty'], delimiter='\t')
        # Skip header row
        next(reader)
        # Clear existing questions
        Question.objects.all().delete()
        # Load new questions from file
        for row in reader:
            Question.objects.create(
                id=row['id'],
                name=row['name'],
                question_swedish=row['question_swedish'],
                answer1_swedish=row['answer1_swedish'],
                answer2_swedish=row['answer2_swedish'],
                answer3_swedish=row['answer3_swedish'],
                answer4_swedish=row['answer4_swedish'],
                question_english=row['question_english'],
                answer1_english=row['answer1_english'],
                answer2_english=row['answer2_english'],
                answer3_english=row['answer3_english'],
                answer4_english=row['answer4_english'],
                area1=row['area1'],
                area2=row['area2'],
                area3=row['area3'],
                difficulty=row['difficulty'],
            )

