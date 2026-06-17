"""
URL configuration for aerodelay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [

path('login_get/',views.login_get),
path('login_post/',views.login_post),
path('forgot_pass/',views.forgot_pass),
path('forgot_pass_post/',views.forgot_pass_post),
path('forgot_pass_postand/',views.forgot_pass_postand),

path('ahome_get/',views.ahome_get),
path('viewairlineoperator_get/',views.viewairlineoperator_get),
path('addairlineoperator_get/',views.addairlineoperator_get),
path('addairlineoperator_post/',views.addairlineoperator_post),
path('addauthority_get/',views.addauthority_get),
path('addauthority_post/',views.addauthority_post),
path('addflightdetails_get/',views.addflightdetails_get),
path('addflightdetails_post/',views.addflightdetails_post),
path('changepassword_get/',views.changepassword_get),
path('editairlineoperator_get/<id>',views.editairlineoperator_get),
path('editairportauthority_get/<id>',views.editairportauthority_get),
path('editflightdetails_get/<id>',views.editflightdetails_get),
path('viewairportauthority_get/',views.viewairportauthority_get),
path('viewflightdetails_get/',views.viewflightdetails_get),
path('viewpassengers_get/',views.viewpassengers_get),
path('editflightdetails_post/',views.editflightdetails_post),
path('editairlineoperator_post/',views.editairlineoperator_post),
path('editairlineoperator_post/',views.editairlineoperator_post),
path('editairportauthority_post/',views.editairportauthority_post),
path('delete_Airline_operator/<id>',views.delete_Airline_operator),
path('delete_Airport_Authority/<id>',views.delete_Airport_Authority),
path('delete_Flight/<id>',views.delete_Flight),
path('changepassword_get/',views.changepassword_get),
path('changepassword_post/',views.changepassword_post),
path('viewcomplaint_get/',views.viewcomplaint_get),
path('viewpassengers_get/',views.viewpassengers_get),
path('o_home_get/',views.o_home_get),
path('o_changepassword_get/',views.o_changepassword_get),
path('o_changepassword_post/',views.o_changepassword_post),
path('viewprofile_get/',views.viewprofile_get),
path('viewflightschedules/<id>',views.viewflightschedules),
path('updatelandingdep_time/<id>',views.updatelandingdep_time),
path('viewflights/',views.viewflights),
path('logout_get/',views.logout_get),
path('sendreply_post/',views.sendreply_post),
path('sendreply/<id>',views.sendreply),


path('addflightshedule/',views.addflightshedule),
path('addflightshedule_post/',views.addflightshedule_post),
path('edit_flight_schedule/<id>', views.edit_flight_schedule),
path('edit_flight_schedule_post/', views.edit_flight_schedule_post),
path('view_flight_schedule/', views.view_flight_schedule),
path('view_flights_autho/', views.view_flights_autho),
path('delete_flight_schedule/<id>', views.delete_flight_schedule),
path('auth_changepassword_get/',views.auth_changepassword_get),
path('auth_changepassword_post/',views.auth_changepassword_post),
path('auth_viewprofile_get/',views.auth_viewprofile_get),
path('authorityhome/',views.authorityhome),
path('airport_congestion/',views.airport_congestion),

path('delay_prediction/<flight_id>',views.delay_prediction),
path('delay_trend_analysis/<flight_id>',views.delay_trend_analysis),
path('frequent_delay_routes/<flight_id>',views.frequent_delay_routes),
path('monitor_delays/<flight_id>',views.monitor_delays),

    path('flutt_login/', views.flutt_login, name='flutt_login'),
    path('passenger_signup/', views.passenger_signup, name='passenger_signup'),
    path('student_change_password/', views.change_password, name='change_password'),

    # Profile
    path('passenger_view_profile/', views.passenger_view_profile, name='passenger_view_profile'),

    # Flight Management
    # In your urls.py
    path('predict_delay/', views.predict_delay, name='predict_delay'),
    path('view_all_flights/', views.view_all_flights, name='view_all_flights'),

    # Favorites
    path('toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('add_to_favourite/', views.add_to_favourite, name='add_to_favourite'),
    path('remove_favourite/', views.remove_favourite, name='remove_favourite'),
    path('remove_multiple_favourites/', views.remove_multiple_favourites, name='remove_multiple_favourites'),
    path('view_favourite_flights/', views.view_favourite_flights, name='view_favourite_flights'),

    # Suggestions
    path('get_flight_suggestions/', views.get_flight_suggestions, name='get_flight_suggestions'),

    # Complaints
    path('passenger_send_complaint/', views.passenger_send_complaint, name='passenger_send_complaint'),
    path('passenger_view_complaints/', views.passenger_view_complaints, name='passenger_view_complaints'),
    path('passenger_view_reply/', views.passenger_view_reply, name='passenger_view_reply'),
    path('passenger_update_profile/', views.passenger_update_profile, name='passenger_update_profile'),
    path('get_prediction_history/', views.get_prediction_history, name='get_prediction_history'),




]
