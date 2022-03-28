from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name="ApiOverview"),
    path('getLights/<str:room>/', views.get_lights, name="getLights"),
    path('getLight/<str:room>/', views.get_light, name="getLight"),
    path('setLight/<str:room>/<str:cmd>/', views.set_light, name="setLight"),
    path('insertLight/', views.insert_light, name="insertLight"),
    # path('updateLight/<str:pk>/', views.update_light, name="updateLight"),
    # path('deleteLight/<str:pk>/', views.delete_light, name="deleteLight"),

    path('weekdayLightOn/<str:room>/<str:time>/',
         views.set_weekday_schedule_light_on, name='weekdayLightOn'),
    path('weekdayLightOff/<str:room>/<str:time>/',
         views.set_weekday_schedule_light_off, name='weekdayLightOff'),
    path('weekendLightOn/<str:room>/<str:time>/',
         views.set_weekend_schedule_light_on, name='weekendLightOn'),
    path('weekendLightOff/<str:room>/<str:time>/',
         views.set_weekend_schedule_light_off, name='weekendLightOff'),
    path('resumeLight/<str:room>/',
         views.resume_schedule_light, name='resumeLight'),
    path('pauseLight/<str:room>/', views.pause_schedule_light, name='pauseLight'),

    path('getTemps/', views.get_temps, name="getTemps"),
    path('getTemp/<str:time>/', views.get_light, name="getTemp"),
    path('setTemp/<str:temp>/', views.set_temp, name="setTemp"),
    path('insertTemp/', views.insert_temp, name="insertTemp"),
]
