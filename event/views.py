from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event
from .models import Square
from .models import MyPlayer
from .models import UserProfile
from .models import Question
import random
from random import shuffle
from django.http import HttpResponse
from django.http import JsonResponse
#import json
import math
from django.contrib.auth import authenticate, login
import string
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from datetime import timedelta

def grid(request):

    grid_size_x = 21
    grid_size_y = 21
    square_size = 30
    grid_extend=10
    
    user=request.user

    myrange=range(0,21)
    myrange_x=range(0,21)
    myrange_y=range(0,21)
    
    if request.method == 'POST':
        
        square_str = request.POST.get('square')
        dropdown_str = request.POST.get('dropdown_value')
        square_str2 = request.POST.get('square2')

        # Get x y of square, or mode
        x, y = square_str.split('*')
        print('y'+str(x))
        print('x'+str(y))
        if x=='answer':
            pass

        elif x=='changemode':
 
            user.userprofile.mode=dropdown_str
            user.userprofile.save()

        elif x=='nav':

            if y=='x+1':
                temp=user.userprofile.x
                user.userprofile.x=temp+1
                user.userprofile.save()
                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
            if y=='x-1':
                temp=user.userprofile.x
                user.userprofile.x=temp-1
                user.userprofile.save()
                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
            if y=='y+1':
                temp=user.userprofile.y
                user.userprofile.y=temp+1
                user.userprofile.save()
                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
            if y=='y-1':
                temp=user.userprofile.y
                user.userprofile.y=temp-1
                user.userprofile.save()
                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)                    

            startx = int(user.userprofile.x)
            stopx = int(user.userprofile.x)+grid_size_x
            starty = int(user.userprofile.y)
            stopy = int(user.userprofile.y)+grid_size_y

            charsx = [str(i) for i in range(startx, stopx)]
            charsy = [str(i) for i in range(starty, stopy)]
            #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
            dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
            #dbsquares = Square.objects.all()
       
            #question = Question.objects.filter(difficulty__lte=1).order_by('?').first()
            question = Question.objects.filter(name='Correct_1').order_by('?').first()
            answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
            shuffle(answers)  # shuffles the answers randomly
            return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares, 'square_size': square_size,'question':question,'answers':answers}) 
       

        else:
            #########################
            #  wants to move
            #########################
            if user.userprofile.mode=="move":
                question = Question.objects.filter(name='Correct_1').order_by('?').first()
                #question = Question.objects.filter(difficulty__lte=2,area1='general').order_by('?').first()

                ###############
                # Qustions set - shouldnt be in grid
                ###############
                #if moveallowed(user.userprofile.xpos,x,user.userprofile.ypos,y):
                if False:

                    user.userprofile.pending_xpos=x
                    user.userprofile.pending_ypos=y
                    user.userprofile.question=question
                    user.userprofile.save()

                    myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                    myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                    squares=get_squares(myrange_x,myrange_y)

                    startx = int(user.userprofile.x)
                    stopx = int(user.userprofile.x)+grid_size_x
                    starty = int(user.userprofile.y)
                    stopy = int(user.userprofile.y)+grid_size_y

                    charsx = [str(i) for i in range(startx-3, stopx+2)]
                    charsy = [str(i) for i in range(starty-3, stopy+2)]
                    #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                    dbsquares = Square.objects.all()
                    #square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                    #################
                    # Question made
                    #################
                    question = user.userprofile.question
                    answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                    shuffle(answers)  # shuffles the answers randomly
                    user.userprofile.question=question
                    user.userprofile.save()

                    return render(request, 'event/home.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'question':question,'answers':answers})





            elif user.userprofile.mode=='paint sea':
                try:
                    square = Square.objects.get(x=x, y=y)
                except Square.DoesNotExist:
                    square = Square.objects.create(x=x, y=y, name='sea4', image='sea.png',)

            elif user.userprofile.mode=='paint land':
                try:
                    square = Square.objects.get(x=x, y=y)
                except Square.DoesNotExist:
                    square = Square.objects.create(x=x, y=y, name='land1', image='land.png',)

            elif user.userprofile.mode=='delete':
                try:
                    square = Square.objects.get(x=x, y=y)
                    square.delete()
                except Square.DoesNotExist:
                    print('no square at there')

            myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
            myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
            squares=get_squares(myrange_x,myrange_y)

            startx = int(user.userprofile.x)
            stopx = int(user.userprofile.x)+grid_size_x
            starty = int(user.userprofile.y)
            stopy = int(user.userprofile.y)+grid_size_y

            charsx = [str(i) for i in range(startx, stopx)]
            charsy = [str(i) for i in range(starty, stopy)]
            #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
            dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
            #dbsquares = Square.objects.all()

        return redirect('grid')
    

    else:

        user = request.user
        myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
        myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
        squares=get_squares(myrange_x,myrange_y)
       
        startx = int(user.userprofile.x)
        stopx = int(user.userprofile.x)+grid_size_x
        starty = int(user.userprofile.y)
        stopy = int(user.userprofile.y)+grid_size_y

        charsx = [str(i) for i in range(startx, stopx)]
        charsy = [str(i) for i in range(starty, stopy)]
        dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
        #dbsquares = Square.objects.all()
        #square_dict = {f"{int(square.y)}-{int(square.x)}": square for square in dbsquares}
        
      
        #question = Question.objects.filter(difficulty__gte=0).order_by('?').first()
        question = Question.objects.filter(name='Correct_1').order_by('?').first()
        return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares,'square_size': square_size,'question':question}) 
        #return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict}) 

def get_squares(xrange,yrange):
    squares = []
    for x in xrange:
        row = []
        for y in yrange:
            try:
                square = Square.objects.get(x=x, y=y)
                image_name = square.image
            except Square.DoesNotExist:
                image_name = 'null.png'
            row.append(image_name)
        squares.append(row)

   
    return squares

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

def grid2(request):
    # Retrieve all Square objects from the database
    squares = Square.objects.all()

    # Pass the squares to the template
    return render(request, 'event/grid.html', {'squares': squares})

def navigate(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    direction = data['direction']
    # Update the x or y values as necessary based on the direction
    # For example:
    if direction == 'up':
      y -= 1
    elif direction == 'down':
      y += 1
    elif direction == 'left':
      x -= 1
    elif direction == 'right':
      x += 1
    # Return a JSON response indicating success
    return JsonResponse({'status': 'success'})
  else:
    # Return an error response if the request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
  



def click(request):
    if request.method == 'POST':
        x = '2'
        y = '2'
        Square.objects.create(x=x, y=y)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})
     

def all_events(request):
    event_list=Event.objects.all()
    return render(request,'event/event_list.html',
        {'event_list':event_list})

def help(request):
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
    grid_size_x = 11
    grid_size_y = 11

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
                #x seems to react on move y
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
                overlays=getLabels(dbsquares)
                return render(request,'event/help.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
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
                overlays=[['name_tag.png',100,100]]
                return render(request,'event/help.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})

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

        # Send ranges,database,question and randomly ordered answers
        myrange_x,myrange_y,dbsquares=getDatabaseAndView(user.userprofile.x,user.userprofile.y,grid_size_x,grid_size_y)
        overlays=getLabels(dbsquares)
        return render(request,'event/help.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})
    # end of if request was post


    else: # if request method was not post

        dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)

        # Send ranges,database,question and randomly ordered answers
        overlays=getLabels(dbsquares)
        return render(request,'event/help.html',{'myrange_x':myrange_x,'myrange_y':myrange_y,'squaredb':dbsquares,'question':question,'answers':answers,'overlays':overlays})



def home(request):
    #delete_inactive_temp_users()
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

    if request.method == 'POST':
        grid_size_x = 11
        grid_size_y = 11
        square_size = 30
        grid_extend=5
    
        user=request.user

        myrange_x=range(0,grid_size_x)
        myrange_y=range(0,grid_size_y)

        square_str = request.POST.get('square')
        dropdown_str = request.POST.get('dropdown_value')
        square_str2 = request.POST.get('square2')

        # Get x y of square, or mode
        x, y = square_str.split('*')
        print('y: '+ str(x))
        print('x: '+ str(y))

        if x=='answer':
            print("answer")
            print(y)
            print(user.userprofile.question.answer1_swedish)
            right_answer=user.userprofile.question.answer1_swedish
            ############################
            # Correct answer
            ############################
            if right_answer == y:

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
                movedy,movedx=getmovedir(user.userprofile.xpos,user.userprofile.ypos,user.userprofile.pending_xpos,user.userprofile.pending_ypos)

                # set new userprofile coordinates
                user.userprofile.xpos=user.userprofile.pending_xpos
                user.userprofile.ypos=user.userprofile.pending_ypos
                user.userprofile.pending_xpos=0
                user.userprofile.pending_ypos=0
                user.userprofile.save()

                # adjust view
                #x seems to react on move y
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

                # get squares between view and view+grid_size
                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                #squares=get_squares(myrange_x,myrange_y)

                # compute the same things as above?
                startx = int(user.userprofile.x)
                stopx = int(user.userprofile.x)+grid_size_x
                starty = int(user.userprofile.y)
                stopy = int(user.userprofile.y)+grid_size_y

                charsx = [str(i) for i in range(startx, stopx)]
                charsy = [str(i) for i in range(starty, stopy)]
                #charsx = [str(i) for i in myrange_x]
                #charsy = [str(i) for i in myrange_y]
                #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
                #dbsquares = Square.objects.all()
                #square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                
                question = Question.objects.filter(name='Correct_1').order_by('?').first()
                user.userprofile.question=question
                user.userprofile.save()
                #question = Question.objects.filter(difficulty__gte=0).order_by('?').first()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                shuffle(answers)  # shuffles the answers randomly
                return render(request, 'event/home.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares, 'square_size': square_size,'question':question,'answers':answers})


            else:
                print('wrong')
                user.userprofile.wrong_answers+=1
                user.userprofile.save()

                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                squares=get_squares(myrange_x,myrange_y)

                startx = int(user.userprofile.x)
                stopx = int(user.userprofile.x)+grid_size_x
                starty = int(user.userprofile.y)
                stopy = int(user.userprofile.y)+grid_size_y

                charsx = [str(i) for i in range(startx, stopx)]
                charsy = [str(i) for i in range(starty, stopy)]
                #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
                #dbsquares = Square.objects.all()
                #square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                question = Question.objects.filter(name='Wrong_1').order_by('?').first()
                user.userprofile.question=question
                user.userprofile.save()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                return render(request, 'event/home.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares, 'square_size': square_size,'question':question,'answers':answers})

        if user.userprofile.mode=="move":
            question = Question.objects.filter(difficulty__lte=2,area1='general').order_by('?').first()

            ###############
            # Qustions set
            ###############
            if moveallowed(user.userprofile.xpos,x,user.userprofile.ypos,y):
                user.userprofile.pending_xpos=x
                user.userprofile.pending_ypos=y
                user.userprofile.question=question
                user.userprofile.save()

                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                squares=get_squares(myrange_x,myrange_y)

                startx = int(user.userprofile.x)
                stopx = int(user.userprofile.x)+grid_size_x
                starty = int(user.userprofile.y)
                stopy = int(user.userprofile.y)+grid_size_y

                #charsx = [str(i) for i in range(startx-grid_extend, stopx+grid_extend)]
                #charsy = [str(i) for i in range(starty-grid_extend, stopy+grid_extend)]

                charsx = [str(i) for i in range(startx, stopx)]
                charsy = [str(i) for i in range(starty, stopy)]
                #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
                #dbsquares = Square.objects.all()
                #square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                    #################
                    # Question made
                    #################
                #question = Question.objects.filter(difficulty__lte=1).order_by('?').first()
                question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                shuffle(answers)  # shuffles the answers randomly
                user.userprofile.question=question
                user.userprofile.save()

                return render(request, 'event/home.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares, 'square_size': square_size,'question':question,'answers':answers})


    grid_size_x = 11
    grid_size_y = 11
    square_size = 30
    user_profile = request.user.userprofile
    user_profile.last_active_time = timezone.now()
    user_profile.save()
    grid_extend=5
    
    
    myrange_x=range(0,grid_size_x)
    myrange_y=range(0,grid_size_y)
    user = request.user
    myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
    myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
    squares=get_squares(myrange_x,myrange_y)
       
    startx = int(user.userprofile.x)
    stopx = int(user.userprofile.x)+grid_size_x
    starty = int(user.userprofile.y)
    stopy = int(user.userprofile.y)+grid_size_y

    charsx = [str(i) for i in range(startx, stopx+grid_extend)]
    charsy = [str(i) for i in range(starty, stopy+grid_extend)]

    charsx = [str(i) for i in range(startx-grid_extend, stopx+grid_extend)]
    charsy = [str(i) for i in range(starty-grid_extend, stopy+grid_extend)]
    #dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
    dbsquares = Square.objects.filter(y__in=charsx,x__in=charsy)
    #dbsquares = Square.objects.all()
    #square_dict = {f"{int(square.y)}-{int(square.x)}": square for square in dbsquares}

    try:
        question = user.userprofile.question
    except:
        question = Question.objects.exclude(area1='utility').filter(difficulty__lte=3).order_by('?').first()
    answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
    return render(request, 'event/home.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'dbsquares':dbsquares, 'square_size': square_size,'question':question,'answers':answers})

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

def getLabels(gottendata):
    return [['name_tag.png',100,100],['name_tag.png',200,200]]