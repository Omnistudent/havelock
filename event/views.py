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

def grid(request):

    grid_size_x = 11
    grid_size_y = 11
    square_size = 30
    
    user=request.user

    myrange=range(0,11)
    myrange_x=range(0,11)
    myrange_y=range(0,11)
    
    if request.method == 'POST':
        
        square_str = request.POST.get('square')
        dropdown_str = request.POST.get('dropdown_value')
        square_str2 = request.POST.get('square2')



        # Get x y of square, or mode
        x, y = square_str.split('*')
        print('xy')
        print(x)
        print(y)
 
        if x=='answer':
            print("answer")
            print(y)
            print(user.userprofile.question.answer1_swedish)
            right_answer=user.userprofile.question.answer1_swedish
            ############################
            # Correct answer
            ############################
            if right_answer == y:
                user.userprofile.correct_answers+=1
                startsquare = Square.objects.get(y=str(user.userprofile.ypos),x=str(user.userprofile.xpos))
                startsquare.occupants3.remove(user.userprofile)
                startsquare.save()

                endsquare = Square.objects.get(x=user.userprofile.pending_xpos, y=user.userprofile.pending_ypos)
                #endsquare = Square.objects.get(x=user.userprofile.pending_xpos, y=user.userprofile.pending_ypos)
                endsquare.occupants3.add(user.userprofile)
                endsquare.save()
                
                movedy,movedx=getmovedir(user.userprofile.xpos,user.userprofile.ypos,user.userprofile.pending_xpos,user.userprofile.pending_ypos)

                
                user.userprofile.xpos=user.userprofile.pending_xpos
                user.userprofile.ypos=user.userprofile.pending_ypos
                user.userprofile.pending_xpos=0
                user.userprofile.pending_ypos=0
                user.userprofile.save()

                
                #seems to react on movey
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


                myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                squares=get_squares(myrange_x,myrange_y)

                startx = int(user.userprofile.x)
                stopx = int(user.userprofile.x)+grid_size_x
                starty = int(user.userprofile.y)
                stopy = int(user.userprofile.y)+grid_size_y

                charsx = [str(i) for i in range(startx-3, stopx+2)]
                charsy = [str(i) for i in range(starty-3, stopy+2)]
                dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                
                question = Question.objects.filter(name='Correct_1').order_by('?').first()
                #question = Question.objects.filter(difficulty__gte=0).order_by('?').first()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                shuffle(answers)  # shuffles the answers randomly
                return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict,'question':question,'answers':answers})


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

                charsx = [str(i) for i in range(startx-3, stopx+2)]
                charsy = [str(i) for i in range(starty-3, stopy+2)]
                dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                question = Question.objects.filter(name='Wrong_1').order_by('?').first()
                answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict,'question':question,'answers':answers})

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

            squares=get_squares(myrange_x,myrange_y)
            startx = int(user.userprofile.x)
            stopx = int(user.userprofile.x)+grid_size_x
            starty = int(user.userprofile.y)
            stopy = int(user.userprofile.y)+grid_size_y

            charsx = [str(i) for i in range(startx-3, stopx+2)]
            charsy = [str(i) for i in range(starty-3, stopy+2)]
            dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
            square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
            question = Question.objects.filter(difficulty__lte=1).order_by('?').first()
            #question = Question.objects.filter(name='Correct_1').order_by('?').first()
            answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
            shuffle(answers)  # shuffles the answers randomly
            return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict,'question':question,'answers':answers}) 
       

        else:
            #########################
            #  wants to move
            #########################
            if user.userprofile.mode=="move":
                print("mooooooooooooooooooove")
                question = Question.objects.filter(difficulty__lte=2,area1='general').order_by('?').first()
                print('question')
                print(question)
                

                user.userprofile.pending_xpos=x
                user.userprofile.pending_ypos=y
                user.userprofile.question=question
                user.userprofile.save()
                ###############
                # Qustions set
                ###############
                if moveallowed(x,y):

                    myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
                    myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
                    squares=get_squares(myrange_x,myrange_y)

                    startx = int(user.userprofile.x)
                    stopx = int(user.userprofile.x)+grid_size_x
                    starty = int(user.userprofile.y)
                    stopy = int(user.userprofile.y)+grid_size_y

                    charsx = [str(i) for i in range(startx-3, stopx+2)]
                    charsy = [str(i) for i in range(starty-3, stopy+2)]
                    dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
                    square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}
                    #################
                    # Question made
                    #################
                    question = user.userprofile.question
                    answers = [question.answer1_swedish, question.answer2_swedish, question.answer3_swedish, question.answer4_swedish]
                    shuffle(answers)  # shuffles the answers randomly
                    print(answers)
                    return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict,'question':question,'answers':answers})

                    #p1=[user.userprofile.xpos,user.userprofile.ypos]
                    #print("userpos is" +str(p1))
                    #p2=[int(x),int(y)]
                    #pdist=math.dist(p1,p2)
                    #if pdist<1.5:
                    #
                    #                 
                   #
                    #    startsquare = Square.objects.get(y=str(user.userprofile.ypos),x=str(user.userprofile.xpos))
                     #   startsquare.occupants3.remove(user.userprofile)
                      #  startsquare.save()
#
 #                       user.userprofile.xpos=int(x)
  #                      user.userprofile.ypos=int(y)
   #                     user.userprofile.save()
#
#                       endsquare = Square.objects.get(x=x, y=y)
 #                       endsquare.occupants3.add(user.userprofile)
  #                      endsquare.save()

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

            myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
            myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
            squares=get_squares(myrange_x,myrange_y)

            startx = int(user.userprofile.x)
            stopx = int(user.userprofile.x)+grid_size_x
            starty = int(user.userprofile.y)
            stopy = int(user.userprofile.y)+grid_size_y

            charsx = [str(i) for i in range(startx-3, stopx+2)]
            charsy = [str(i) for i in range(starty-3, stopy+2)]
            dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
            square_dict = {f"{square.x}*{square.y}": square for square in dbsquares}

            
            #dbsquares = Square.objects.all() 

        return redirect('grid')
    

    else:

        user = request.user
        myrange_x=range(user.userprofile.x,int(user.userprofile.x)+grid_size_x)
        myrange_y=range(user.userprofile.y,int(user.userprofile.y)+grid_size_y)
        squares=get_squares(myrange_x,myrange_y)
        #for square in Square.objects.all():
        #    square.image = square.image.replace('image.png', 'sea.png')
        #    square.save()


        #dbsquares = Square.objects.filter(image="event/image.png")
        #try:
        #    dbsquare = Square.objects.get(x='4', y='4')
        #    dbsquare.occupants3.add(user.userprofile)
        #    dbsquare.save()
        #    print(dbsquare.occupants3)
        #except:
        #    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        #dbsquare.occupants3.add(user.userprofile)
        
        #dbsquares = Square.objects.all()
        #dbsquares = Square.objects.all()
        startx = int(user.userprofile.x)
        stopx = int(user.userprofile.x)+grid_size_x
        starty = int(user.userprofile.y)
        stopy = int(user.userprofile.y)+grid_size_y

        charsx = [str(i) for i in range(startx-3, stopx+2)]
        charsy = [str(i) for i in range(starty-3, stopy+2)]
        dbsquares = Square.objects.filter(x__in=charsx,y__in=charsy)
        square_dict = {f"{int(square.y)}-{int(square.x)}": square for square in dbsquares}
        
        #for squared in dbsquares:
        #    squared.occupants3.remove(user.userprofile)
        #    squared.save()
        
        #for i in dbsquares:
        #    print(i.occupants3.all())
        question = Question.objects.filter(difficulty__gte=0).order_by('?').first()
        return render(request, 'event/grid.html', {'myrange_x':myrange_x,'myrange_y':myrange_y,'myrange':myrange,'dbsquares':dbsquares,'squares': squares, 'square_size': square_size,'dbdic':square_dict,'question':question}) 
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

def moveallowed(x,y):
    #endsquare = Square.objects.get(x=x, y=y)
    #if endsquare.image=='land.png':
    #    return False
    return True

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


def home(request,year=datetime.now().year,month="March"):
    name="Theo"
    month=month.title()
    month_number=list(calendar.month_name).index(month)
    month_number=int(month_number)

    cal=HTMLCalendar().formatmonth(
        year,
        month_number)

    #now=datetime.now()
    #current_year=now.year

    return render(request,
    'event/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
    })

def getmovedir(xstart,ystart,xend,yend):
    dx=int(int(xend)-int(xstart))
    dy=int(yend-ystart)
    return (dx,dy)