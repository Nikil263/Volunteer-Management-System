from django.contrib import admin
from django.urls import path
from . import views
from . import v_controller

urlpatterns = [
    path('', views.login_view),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
  #  path('homepage/', views.homepage, name='homepage'),
    path('setting/<int:userType>/', v_controller.setting, name='setting'),

    
    #path('setting/', v_controller.setting, name='setting'),
    path('update_setting/', v_controller.updateOrgSetting, name='update_setting'),
    path('update_profile/', v_controller.update_profile, name='update_profile'),
     path('event_creation/<str:username>/', v_controller.event_creation, name='event_creation'),
     path('deleteEvent/<int:eventId>/<str:username>/', v_controller.deleteEvent, name='deleteEvent'),
  path('loadHomepage/<str:username>/', v_controller.loadHomepage, name='loadHomepage'),
    path('registerEvent/<int:eventId>/<str:username>/', v_controller.registerEvent, name='registerEvent'),
  path('unRegisterEvent/<int:eventId>/<str:username>/', v_controller.unRegisterEvent, name='unRegisterEvent'),
    path('myEvents/<str:username>/', v_controller.myEvents, name='myEvents'),
  path('volunteerEvents/<str:username>/', v_controller.volunteerEvents, name='volunteerEvents'),
  path('logout/', views.logouts, name='logout'),
  path('event-details/<int:eventId>/<str:username>/', v_controller.eventDetails, name='eventDetails')

    






  
     


    


]
