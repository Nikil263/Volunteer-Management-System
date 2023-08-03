from django.shortcuts import render
from .models import Profile, Organization, Volunteer, Event

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
#from profileapp.models import Profile

def setting(request, userType):
    return render(request, 'settings.html', {'user_type': userType,'username': request.user})

def updateOrgSetting(request):
    if request.method == 'POST':
        # userType = request.POST.get('userType')
        # print("the new value of the usertype = ", userType)
        user = request.user
        profile = get_object_or_404(Profile, userName=user)

        # # Modify the volunteer field
        # profile.userType = userType
        # profile.save()

        orgName = request.POST.get('orgName')
        orgDivision = request.POST.get('orgDivision')
        
        try:
            organization = Organization.objects.get(profile=profile)
            organization.profile = profile
            organization.orgName = orgName
            organization.orgDivision = orgDivision
            organization.save()
        except:
            organization = Organization(profile=profile, orgName=orgName, orgDivision=orgDivision)
            organization.save()


        message = "Settings updated"
        userName = request.user.username
        return redirect("/loadHomepage/" + userName + "/")
    else:
        return render(request, 'registrationapp/login.html')

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(Profile, userName=user)
        skills = request.POST.get('skills')
        highLevelEducation = request.POST.get('education')
        try:
            volunteer = Volunteer.objects.get(profile=profile)
            volunteer.profile = profile
            volunteer.skills = skills
            volunteer.highLevelEducation = highLevelEducation
            volunteer.save()
        except:
            volunteer = Volunteer(profile=profile, skills=skills, highLevelEducation=highLevelEducation)
            volunteer.save()
        message = "Your skills have been saved"
        allEvents = Event.objects.all()
        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'username': user, 'events': allEvents})
        # return render(request, 'volPage.html', {'e': event})

def event_creation(request,username):
    if request.method == 'POST':
        eventName = request.POST['event_name']
        profile = get_object_or_404(Profile, userName=request.user)
        organization = get_object_or_404(Organization, profile=profile)
        event_description = request.POST['event_description']
        event_type = request.POST['event_type']
        no_of_positions = int(request.POST['no_of_positions'])
        location = request.POST['location']
        date = request.POST['date']
        stime = request.POST['stime']
        etime = request.POST['etime']
        
        # Create event under the organization
        event = Event.objects.create(eventName=eventName, organization=organization, eventDescription=event_description, eventType=event_type, noOfPositions=no_of_positions, location=location, eventDate=date, startTime=stime, endTime=etime)
        
        event.save()
        message = "Event has been saved"
        #event = Event.objects.all()
        userName = request.user.username
        return redirect("/loadHomepage/" + userName + "/")
        #return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'username':request.user.username})
        # return render(request, 'volPage.html', {'e': event})
    else:
        return render(request, 'event_creation.html', {'message': 'hi', 'user_type': 2, 'username': request.user})

def deleteEvent(request, eventId, username):
    event = Event.objects.get(id=eventId)
    event.delete()
    # print(User.username)
    profile = Profile.objects.get(userName = username)
    # print(user)
    print(profile)
    allEvents = []
    message = ""
    if profile.userType==1:
        print("volunteer")
        return render(request, 'homepage.html', {'message': message, 'user_type': 1})
    else:
        try:
            organization = Organization.objects.get(profile=profile)
            allEvents = Event.objects.filter(organization = organization)
            print(allEvents)
        except:
            organization = ""
        print("organizer")
        return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})
    
def loadHomepage(request, username):
    # print(User.username)
    profile = Profile.objects.get(userName = username)
    # print(user)
    print(profile)
    allEvents = []
    message = ""
    if profile.userType==1:
        print("volunteer")
        allEvents = Event.objects.all()
        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'username': username, 'events': allEvents})
    else:
        try:
            organization = Organization.objects.get(profile=profile)
            allEvents = Event.objects.filter(organization = organization)
            print(allEvents)
        except:
            organization = ""
        print("organizer")
        return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})

def registerEvent(request, eventId, username):

    print("register event ")
    print(eventId)
    print(username)
    profile = Profile.objects.get(userName = username)
    if not Volunteer.objects.filter(profile=profile).exists():
        message = "Please update Profile before registering for events"
        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})
    
    



    
    volunteer = Volunteer.objects.get(profile=profile)
    event = Event.objects.get(id=eventId)
    if event.noOfPositions != 0:
        volunteer.event.add(event)
        event.noOfPositions = event.noOfPositions-1
        event.save()
        message = "Registered for event " + event.eventName + " successfully."
    else:
        message = "You are late."

    #volunteer.save()
    # event.delete()
    # # print(User.username)
    # profile = Profile.objects.get(userName = username)
    # # print(user)
    # print(profile)
    allEvents = []
    
    
    return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})

def myEvents(request, username):
    profile = Profile.objects.get(userName = username)
    volunteer = Volunteer.objects.get(profile=profile)
    event = volunteer.event.all()

    print(event)
    
    return render(request, 'my_events.html', {'user_type': 1, 'events': event, 'username': username})

def unRegisterEvent(request, eventId, username):

    print("register event ")
    print(eventId)
    print(username)
    profile = Profile.objects.get(userName = username)
    volunteer = Volunteer.objects.get(profile=profile)
    event = Event.objects.get(id=eventId)
    volunteer.event.remove(event)
    event.noOfPositions = event.noOfPositions + 1
    event.save()
    #volunteer.save()
    # event.delete()
    # # print(User.username)
    # profile = Profile.objects.get(userName = username)
    # # print(user)
    # print(profile)
    allEvents = []
    message = "Unregistered for event " + event.eventName + " successfully."
    
    return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})

def volunteerEvents(request, username):

    print("register event ")
    # print(eventId)
    print(username)
    profile = Profile.objects.get(userName = username)
    organization = Organization.objects.get(profile=profile)
    events = Event.objects.filter(organization=organization)
    message = ""
    return render(request, 'voluteer_event.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})
    

def eventDetails(request, eventId, username):

    print("register event ")
    # print(eventId)
    print(username)
    
    events = Event.objects.get(id=eventId)
    message = ""
    return render(request, 'eventdetail.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})