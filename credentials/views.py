from django.shortcuts import render
from .models import Profile, Organization, Event
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
#from profileapp.models import Profile

def signup(request):
    if request.method == 'POST':
        firstName = request.POST['name']
        lastName = request.POST['lastname']
        userName = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        userType = request.POST['userType']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
                return redirect('signup')
            elif User.objects.filter(username=userName).exists():
                messages.info(request, 'username already exists')
                return redirect('signup')
            else:
                #user = User.objects.create_user(name=name, lastname=lastname, username=username, email=email, password=password)
                user = User.objects.create_user(username=userName, email=email, password=password)
                user.save()

                userProfile = Profile(firstName=firstName, lastName=lastName, userType=userType, userName=user)
                userProfile.save()

                # user_model = User.objects.get(username=username)
                # new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                # new_profile.save()
                return redirect('/login/')
        
        else:
            messages.info(request, "passwords do not match")
            return redirect('signup/')
            
    return render(request, "registrationapp/signup.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User credentials are valid, log the user in
            login(request, user)
            message = "login successful"
            profile = Profile.objects.get(userName=username)

            
            print(user)
            
            print(profile)
            allEvents = []
            if profile.userType==1:
                events = Event.objects.all()
                print("volunteer")
                return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})
            else:
                try:
                    organization = Organization.objects.get(profile=profile)
                    allEvents = Event.objects.filter(organization = organization)
                    print(allEvents)
                except:
                    organization = ""
                                    
                
                
                print("organizer")
                return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})
            
        else:
            # User credentials are invalid, display an error message
            message = "Invalid username or password"
            return render(request, 'registrationapp/login.html', {'message': message})
    else:
        return render(request, 'registrationapp/login.html')

# def updateType(request):
#     if request.method == 'POST':
#         userType = request.POST.get('userType')
#         user = request.user
#         profile = get_object_or_404(Profile, userName=user)

#         # Modify the volunteer field
#         profile.userType = userType
#         profile.save()

#         message = "Settings updated"
#         return render(request, 'registrationapp/login.html', {'message': message})
#     else:
#         return render(request, 'registrationapp/login.html')

def logouts(request):
    logout(request)
    return redirect('/')