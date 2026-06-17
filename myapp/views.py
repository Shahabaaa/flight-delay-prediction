from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from myapp.models import *


def login_get(request):
    return render(request,'login.html')



def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    print(request.POST)
    ll=authenticate(request,username=username,password=password)
    print(ll,"===")
    if ll is not None:
        login(request,ll)
        if ll.groups.filter(name="Admin"):
            return redirect('/myapp/ahome_get/')

        elif ll.groups.filter(name="AirlineOperator"):
            return redirect('/myapp/o_home_get/')
        elif ll.groups.filter(name="AirportAuthority"):
            return redirect('/myapp/authorityhome/')

        else:
            return redirect('/myapp/login_get/')
    else:
        return redirect('/myapp/login_get/')


def forgot_pass(request):
    return render(request,'forgotpassword.html')


from django.core.mail import send_mail
from django.conf import settings
def forgot_pass_post(request):
    username=request.POST['username']
    ll=User.objects.filter(username=username)
    if ll.exists():
        psw=random.randint(0000000,9999999)
        h=User.objects.get(username=username)
        h.set_password(str(psw))
        h.save()
        send_mail("Temp password", str(psw), settings.EMAIL_HOST_USER, [username])

        return redirect('/myapp/login_get/')

    else:
        return redirect('/myapp/forgot_pass/')

def forgot_pass_postand(request):
    username = request.POST['email']
    ll = User.objects.filter(username=username)
    if ll.exists():
        psw=random.randint(0000000,9999999)
        h = User.objects.get(username=username)
        h.set_password(str(psw))
        h.save()
        send_mail("Temp password", str(psw), settings.EMAIL_HOST_USER, [username])

        return JsonResponse({'status':'ok'})

    else:
        return JsonResponse({'status':'no'})

# user=User.objects.get(username="admin@gmail.com")
# user.set_password('12345')
# user.save()



def ahome_get(request):
    return render(request,'Admin/home_index.html')


def viewairlineoperator_get(request):
    data=Airline_Operator.objects.all()
    return render(request,'Admin/viewairlineoperator.html',{'data':data})


def addauthority_get(request) :
    return render(request,'Admin/addauthority.html')



def addauthority_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    city=request.POST['city']
    state=request.POST['state']
    District=request.POST['district']
    Post=request.POST['post']
    pincode=request.POST['pincode']
    photo=request.FILES['photo']
    proof=request.FILES['proof']
    print(name,gender,'hvhjvjhv')


    if Airport_Authority.objects.filter(Email=email).exists():
        messages.warning(request,'Email already exists')
        return redirect('/myapp/addauthority_get/')

    user=User.objects.create_user(username=email,password=phone)
    user.groups.add(Group.objects.get(name='AirportAuthority'))
    user.save()

    fs=FileSystemStorage()
    date=datetime.now().strftime('%y%m%d-%H%M%S')+".jpg"
    date2=datetime.now().strftime('%y%m%d-%H%M%S')+"1.jpg"
    fs.save(date,photo)
    fs.save(date2,proof)
    path=fs.url(date)
    path2=fs.url(date2)

    obj=Airport_Authority()
    obj.Full_Name=name
    obj.Email=email
    obj.Phone=phone
    obj.Gender=gender
    obj.DOB=dob
    obj.Photo=photo
    obj.Place=place
    obj.Post=Post
    obj.City=city
    obj.District=District
    obj.State=state
    obj.Pincode=pincode
    obj.Proof=path2
    obj.Photo=path
    obj.AUTHUSER=user
    obj.save()

    return redirect('/myapp/viewairportauthority_get/#abc')



def addairlineoperator_get(request) :
    return render(request,'Admin/addairlineoperator.html')


def addairlineoperator_post(request):
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    city=request.POST['city']
    state=request.POST['state']
    district=request.POST['district']
    post=request.POST['post']
    pincode=request.POST['pincode']
    photo=request.FILES['photo']
    proof=request.FILES['proof']

    if User.objects.filter(username=email).exists():
        messages.warning(request,'Email already exists')
        return redirect('/myapp/addairlineoperator_get/')


    if Airline_Operator.objects.filter(Phone = phone).exists():
        messages.warning(request,'Phone already exists')
        return redirect('/myapp/addairlineoperator_get/')


    user = User.objects.create(username=email, password=make_password(phone))
    user.groups.add(Group.objects.get(name='AirlineOperator'))

    fs = FileSystemStorage()
    date = datetime.now().strftime('%y%m%d-%H%M%S') + ".jpg"
    date2 = datetime.now().strftime('%y%m%d-%H%M%S') + "1.jpg"
    fs.save(date, photo)
    fs.save(date2, proof)
    path = fs.url(date)
    path2 = fs.url(date2)


    obj = Airline_Operator()
    obj.Full_Name = name
    obj.Email = email
    obj.Phone = phone
    obj.gender = gender
    obj.DOB = dob
    obj.Photo = photo
    obj.Place = place
    obj.Post = post
    obj.City = city
    obj.District = district
    obj.State = state
    obj.Pincode = pincode
    obj.Proof = path2
    obj.Photo = path
    obj.AUTHUSER = user
    obj.save()
    messages.success(request, 'successfully added')
    return redirect('/myapp/viewairlineoperator_get/#abc')

def addflightdetails_get(request):
    return render(request,'Admin/addflightdetails.html')

def addflightdetails_post(request):
    FlightName=request.POST['FlightName']
    Source=request.POST['Source']
    Destination=request.POST['Destination']
    Date=request.POST['Date']
    Time=request.POST['Time']


    if Flight.objects.filter(Flight_Name = FlightName).exists():
        messages.warning(request,'Flight already exists')
        return redirect('/myapp/addflightdetails_get/')



    a=Flight()
    a.Flight_Name=FlightName
    a.Source=Source
    a.Destination=Destination
    a.Date=Date
    a.Time=Time
    a.save()
    messages.success(request, 'successfully added')
    return redirect('/myapp/viewflightdetails_get/#abc')



def editflightdetails_get(request,id) :
    a=Flight.objects.get(id=id)
    return render(request,'Admin/editflightdetails.html',{'data':a})

def editflightdetails_post(request):
    FlightName=request.POST['FlightName']
    Source=request.POST['Source']
    Destination=request.POST['Destination']
    Date=request.POST['Date']
    Time=request.POST['Time']
    id=request.POST['id']


    a=Flight.objects.get(id=id)
    a.Flight_Name=FlightName
    a.Source=Source
    a.Destination=Destination
    a.Date=Date
    a.Time=Time
    a.save()
    messages.success(request, 'successfully edited')
    return redirect('/myapp/viewflightdetails_get/#abc')

def delete_Flight(request,id):
    Flight.objects.get(id=id).delete()
    return redirect('/myapp/viewflightdetails_get/')

def changepassword_get(request) :
    return render(request,'Admin/changepassword.html')
def changepassword_post(request):
    current = request.POST['current']
    new = request.POST['new']
    confirm = request.POST['confirm']

    user=request.user
    if user.check_password(current):
        if new == confirm:
            user.set_password(new)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/changepassword_get/')
    else:
        return redirect('/myapp/changepassword_get/')





def editairlineoperator_get(request,id) :
    a=Airline_Operator.objects.get(id=id)
    return render(request,'Admin/editairlineoperator.html',{'data':a})

def editairlineoperator_post(request):
    name = request.POST['Full_Name']
    gender = request.POST['gender']
    dob = request.POST['DOB']
    email = request.POST['Email']
    phone = request.POST['Phone']
    place = request.POST['Place']
    city = request.POST['City']
    state = request.POST['State']
    district = request.POST['District']
    post = request.POST['Post']
    pincode = request.POST['Pincode']
    id = request.POST['id']
    obj = Airline_Operator.objects.get(id=id)



    if 'photo' in request.FILES:
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        date = datetime.now().strftime('%y%m%d-%H%M%S') + ".jpg"
        fs.save(date, photo)
        path = fs.url(date)
        obj.Photo = path
        obj.save()

    if 'proof' in request.FILES:
        proof = request.FILES['proof']

        fs = FileSystemStorage()
        date2 = datetime.now().strftime('%y%m%d-%H%M%S') + "1.jpg"
        fs.save(date2, proof)
        path2 = fs.url(date2)
        obj.Proof = path2

        obj.save()



    obj.Full_Name = name
    obj.Email = email
    obj.Phone = phone
    obj.gender = gender
    obj.DOB = dob
    obj.Place = place
    obj.post = post
    obj.City = city
    obj.District = district
    obj.State = state
    obj.Pincode = pincode
    obj.save()
    return redirect('/myapp/viewairlineoperator_get/')


def delete_Airline_operator(request,id):
    Airline_Operator.objects.get(AUTHUSER=id).delete()
    User.objects.get(id=id).delete()
    return redirect('/myapp/viewairlineoperator_get')

def delete_Airport_authority(request,id):
    g=Airport_Authority.objects.get(id=id)
    User.objects.get(id=g.AUTHUSER).delete()
    return redirect('/myapp/viewairportauthority_get')

def editairportauthority_get(request,id) :
    a=Airport_Authority.objects.get(id=id)
    return render(request,'Admin/editairportauthoriy.html',{'data':a})

def editairportauthority_post(request):
    name = request.POST['Full_Name']
    gender = request.POST['Gender']
    dob = request.POST['DOB']
    Email = request.POST['Email']
    phone = request.POST['Phone']
    place = request.POST['Place']
    city = request.POST['City']
    State = request.POST['State']
    district = request.POST['District']
    post = request.POST['Post']
    pincode = request.POST['Pincode']
    id = request.POST['id']


    obj = Airport_Authority.objects.get(id=id)


    if 'Photo' in request.FILES:
        photo = request.FILES['Photo']
        fs1 = FileSystemStorage()
        date1 = datetime.now().strftime('%y%m%d-%H%M%S') + ".jpg"
        fs1.save(date1, photo)
        path1 = fs1.url(date1)
        obj.Photo = path1
        obj.save()


    if 'Proof' in request.FILES:
        proof = request.FILES['Proof']
        date2 = datetime.now().strftime('%y%m%d-%H%M%S') + "1.jpg"
        fs2 = FileSystemStorage()
        fs2.save(date2, proof)
        path2 = fs2.url(date2)
        obj.Proof = path2
        obj.save()


    obj.Full_Name = name
    obj.Email = Email
    obj.Phone = phone
    obj.Gender = gender
    obj.DOB = dob
    obj.Place = place
    obj.Post = post
    obj.City = city
    obj.District = district
    obj.State = State
    obj.Pincode = pincode
    obj.save()

    return redirect('/myapp/viewairportauthority_get/')



def delete_Airport_Authority(request,id):
    Airport_Authority.objects.get(AUTHUSER=id).delete()
    User.objects.get(id=id).delete()
    return redirect('/myapp/viewairportauthority_get/')

def logout_get(request):
    logout(request)
    return redirect('/myapp/login_get/')

# def editflightdetails_get(request) :
#     return render(request,'Admin/editflightdetails.html')
#
# def editflightdetails_post(request):
#     name = request.POST['name']
#     gender = request.POST['gender']
#     dob = request.POST['dob']
#     email = request.POST['email']
#     phone = request.POST['phone']
#     place = request.POST['place']
#     city = request.POST['city']
#     state = request.POST['state']
#     district = request.POST['district']
#     post = request.POST['post']
#     pincode = request.POST['pincode']
#     photo = request.FILES['photo']
#     proof = request.FILES['proof']
#
#     a=Flight
#
#     return redirect('/myapp//')

def viewairportauthority_get(request) :
    a=Airport_Authority.objects.all()
    return render(request,'Admin/viewairportauthority.html',{'data':a})

def viewflightdetails_get(request) :
    a=Flight.objects.all()
    return render(request,'Admin/viewflightdetails.html',{'data':a})

def viewpassengers_get(request) :
    a = Passenger.objects.all()
    return render(request,'Admin/viewpassengers.html',{'data':a})

def viewcomplaint_get(request) :
    a=Complaint.objects.all()
    return render(request,'Admin/viewcomplaint.html',{'data':a})


def sendreply(request,id):
    request.session['cid']=id
    return render(request,'Admin/send reply.html')

def sendreply_post(request):
    reply = request.POST['reply']
    id = request.session['cid']
    Complaint.objects.filter(id=id).update(Status="Replied",Reply=reply)

    return redirect('/myapp/viewcomplaint_get/')




#======Operator=============

def o_home_get(request):
    return render(request,'Airline Operator/homeindex.html')

def o_changepassword_get(request):
    return render(request,'Airline Operator/changepassword.html')

def o_changepassword_post(request):
    current = request.POST['current']
    new = request.POST['new']
    confirm = request.POST['confirm']

    user = User.objects.get(id=request.user.id)
    if user.check_password(current):
        if new == confirm:
            user.set_password(new)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/o_changepassword_get/')
    else:
        return redirect('/myapp/o_changepassword_get/')


def viewprofile_get(request):
    data=Airline_Operator.objects.get(AUTHUSER=request.user)
    return render(request,'Airline operator/viewprofile.html',{'data':data})


def viewflightschedules(request,id):
    data=Flight_Schedule.objects.filter(FLIGHT=id)
    return render(request,'Airline operator/viewflightschedules.html',{'data':data})

def viewflights(request):
    data=Flight.objects.all()
    return render(request,'Airline operator/viewflightdetails.html',{'data':data})

def updatelandingdep_time(request, id):

    schedule = Flight_Schedule.objects.get(id=id)

    try:
        data = Flight_LandingdepTime.objects.get(FLIGHTSCHEDULE=schedule)
    except:
        data = None

    if request.method == "POST":

        arrival = request.POST['arrival']
        depart = request.POST['depart']

        if data:   # UPDATE
            data.arrivaltime = arrival
            data.departtime = depart
            data.save()

        else:      # ADD
            Flight_LandingdepTime.objects.create(
                Date=datetime.now().date(),
                Time=datetime.now().time(),
                arrivaltime=arrival,
                departtime=depart,
                FLIGHTSCHEDULE=schedule
            )

        return redirect('/myapp/updatelandingdep_time/'+str(id))

    return render(request,'Airline operator/updatearrivaldep.html',{
        'data':data,
        'schedule':schedule
    })



# ================authority==============================

def addflightshedule(request):
    flights=Flight.objects.all()
    return render(request,'authority/addflightschedules.html',{'flights':flights})

def addflightshedule_post(request):
    flight_id = request.POST['flight_id']
    date = request.POST['flight_date']
    dep = request.POST['scheduled_departure']
    arr = request.POST['scheduled_arrival']

    flight = Flight.objects.get(id=flight_id)

    Flight_Schedule.objects.create(
        FLIGHT=flight,
        Flight_Date=date,
        Scheduled_Departure=dep,
        Scheduled_Arrival=arr
    )

    return redirect('/myapp/addflightshedule/')


def edit_flight_schedule(request, id):
    schedule = Flight_Schedule.objects.get(id=id)
    flights = Flight.objects.all()
    return render(request, "authority/editflightschedules.html", {
        "data": schedule,
        "flights": flights
    })

def edit_flight_schedule_post(request):
    id = request.POST['id']
    flight_id = request.POST['flight_id']
    flight_date = request.POST['flight_date']
    departure = request.POST['scheduled_departure']
    arrival = request.POST['scheduled_arrival']

    schedule = Flight_Schedule.objects.get(id=id)

    flight = Flight.objects.get(id=flight_id)

    schedule.FLIGHT = flight
    schedule.Flight_Date = flight_date
    schedule.Scheduled_Departure = departure
    schedule.Scheduled_Arrival = arrival

    schedule.save()

    return redirect('/myapp/view_flight_schedule/')

def delete_flight_schedule(request, id):
    schedule = Flight_Schedule.objects.get(id=id)
    schedule.delete()
    return redirect('/myapp/view_flight_schedule/')

def view_flight_schedule(request):
    data = Flight_Schedule.objects.all()
    return render(request,'authority/viewflightschedules.html',{'data':data})
def view_flights_autho(request):
    data = Flight.objects.all()
    return render(request,'authority/viewflightdetails.html',{'data':data})


def auth_changepassword_get(request):
    return render(request,'authority/changepassword.html')

def auth_changepassword_post(request):
    current = request.POST['current']
    new = request.POST['new']
    confirm = request.POST['confirm']

    user = User.objects.get(id=request.user.id)
    if user.check_password(current):
        if new == confirm:
            user.set_password(new)
            user.save()
            logout(request)
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/auth_changepassword_get/')
    else:
        return redirect('/myapp/auth_changepassword_get/')

def auth_viewprofile_get(request):
    data=Airport_Authority.objects.get(AUTHUSER=request.user)
    return render(request,'authority/viewprofile.html',{'data':data})

def authorityhome(request):
    return render(request,'authority/homeindex.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import io
import base64
import os
from .models import Flight, Flight_Schedule, Flight_LandingdepTime


def delay_prediction(request, flight_id):
    try:
        # Get flight details
        flight = Flight.objects.get(id=flight_id)

        # Get all schedules for this flight ordered by date
        schedules = Flight_Schedule.objects.filter(FLIGHT=flight).order_by('Flight_Date')

        if not schedules.exists():
            messages.error(request, "No flight schedules found for this flight")
            return redirect('/myapp/viewflights/')

        # Helper function to convert time string to minutes
        def time_to_minutes(time_str):
            try:
                if len(str(time_str).split(':')) == 3:
                    t = datetime.strptime(str(time_str), '%H:%M:%S').time()
                else:
                    t = datetime.strptime(str(time_str), '%H:%M').time()
                return t.hour * 60 + t.minute
            except:
                return 0

        # Helper function to convert minutes to time string
        def minutes_to_time(minutes):
            hours = (int(minutes) // 60) % 24
            mins = int(minutes) % 60
            return f"{hours:02d}:{mins:02d}"

        # Prepare training data
        features = []
        targets = []
        dates = []

        for schedule in schedules:
            actual_times = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

            if actual_times:
                scheduled_dep = time_to_minutes(schedule.Scheduled_Departure)
                scheduled_arr = time_to_minutes(schedule.Scheduled_Arrival)
                actual_dep = time_to_minutes(actual_times.departtime)
                actual_arr = time_to_minutes(actual_times.arrivaltime)

                dep_delay = actual_dep - scheduled_dep
                arr_delay = actual_arr - scheduled_arr

                feature = [
                    scheduled_dep,
                    scheduled_arr,
                    schedule.Flight_Date.month,
                    schedule.Flight_Date.day,
                    schedule.Flight_Date.weekday(),
                ]

                features.append(feature)
                targets.append([dep_delay, arr_delay])
                dates.append(schedule.Flight_Date)

        # Train model and make predictions
        has_model = False
        historical_predictions = []
        future_predictions = []
        graph = None

        if len(features) >= 10:
            X = np.array(features, dtype=np.float32)
            y = np.array(targets, dtype=np.float32)

            scaler_X = MinMaxScaler()
            scaler_y = MinMaxScaler()

            X_scaled = scaler_X.fit_transform(X)
            y_scaled = scaler_y.fit_transform(y)

            sequence_length = min(5, len(X_scaled) - 1)
            X_seq, y_seq = [], []

            for i in range(len(X_scaled) - sequence_length):
                X_seq.append(X_scaled[i:i + sequence_length])
                y_seq.append(y_scaled[i + sequence_length])

            X_seq = np.array(X_seq, dtype=np.float32)
            y_seq = np.array(y_seq, dtype=np.float32)

            if len(X_seq) > 0:
                # Build and train LSTM model
                model = Sequential([
                    LSTM(50, return_sequences=True, input_shape=(X_seq.shape[1], X_seq.shape[2])),
                    Dropout(0.2),
                    LSTM(50, return_sequences=True),
                    Dropout(0.2),
                    LSTM(50),
                    Dropout(0.2),
                    Dense(2)
                ])

                model.compile(optimizer='adam', loss='mse')
                model.fit(X_seq, y_seq, epochs=30, batch_size=16, verbose=0, validation_split=0.2)

                has_model = True

                # ============================================
                # PART 1: Predictions for HISTORICAL flights (for validation)
                # ============================================
                for i in range(max(0, len(schedules) - 10), len(schedules)):
                    schedule = schedules[i]
                    if i >= sequence_length:
                        pred_seq = X_scaled[i - sequence_length:i].reshape(1, sequence_length, -1)
                        pred_scaled = model.predict(pred_seq, verbose=0)
                        pred = scaler_y.inverse_transform(pred_scaled)[0]

                        scheduled_dep_min = time_to_minutes(schedule.Scheduled_Departure)
                        scheduled_arr_min = time_to_minutes(schedule.Scheduled_Arrival)

                        # Get actual values if they exist
                        actual = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

                        historical_predictions.append({
                            'date': schedule.Flight_Date,
                            'scheduled_dep': schedule.Scheduled_Departure,
                            'scheduled_arr': schedule.Scheduled_Arrival,
                            'pred_dep_delay': round(pred[0], 2),
                            'pred_arr_delay': round(pred[1], 2),
                            'pred_dep_time': minutes_to_time(scheduled_dep_min + pred[0]),
                            'pred_arr_time': minutes_to_time(scheduled_arr_min + pred[1]),
                            'actual_dep_time': actual.departtime if actual else 'N/A',
                            'actual_arr_time': actual.arrivaltime if actual else 'N/A',
                            'type': 'historical'
                        })

                # ============================================
                # PART 2: Predictions for FUTURE flights
                # ============================================
                last_schedule = schedules.last()
                last_date = last_schedule.Flight_Date

                # Get the last sequence for future predictions
                last_sequence = X_scaled[-sequence_length:].reshape(1, sequence_length, -1)

                # Predict for next 7 days
                for days_ahead in range(1, 8):  # Next 7 days
                    future_date = last_date + timedelta(days=days_ahead)

                    # Skip weekends if needed (optional)
                    # if future_date.weekday() in [5, 6]:  # Saturday, Sunday
                    #     continue

                    # Make prediction
                    pred_scaled = model.predict(last_sequence, verbose=0)
                    pred = scaler_y.inverse_transform(pred_scaled)[0]

                    # Use the same scheduled times as the last flight (or you can vary them)
                    scheduled_dep_min = time_to_minutes(last_schedule.Scheduled_Departure)
                    scheduled_arr_min = time_to_minutes(last_schedule.Scheduled_Arrival)

                    # Add small variations to scheduled times for different days
                    if days_ahead % 2 == 0:
                        scheduled_dep_min += 30  # Alternate flights at different times
                        scheduled_arr_min += 30

                    future_predictions.append({
                        'date': future_date,
                        'scheduled_dep': minutes_to_time(scheduled_dep_min),
                        'scheduled_arr': minutes_to_time(scheduled_arr_min),
                        'pred_dep_delay': round(pred[0], 2),
                        'pred_arr_delay': round(pred[1], 2),
                        'pred_dep_time': minutes_to_time(scheduled_dep_min + pred[0]),
                        'pred_arr_time': minutes_to_time(scheduled_arr_min + pred[1]),
                        'day': future_date.strftime('%A'),
                        'type': 'future'
                    })

                    # Update the sequence for next prediction (rolling)
                    new_feature = [
                        scheduled_dep_min,
                        scheduled_arr_min,
                        future_date.month,
                        future_date.day,
                        future_date.weekday(),
                    ]
                    new_feature_scaled = scaler_X.transform([new_feature])
                    last_sequence = np.roll(last_sequence, -1, axis=1)
                    last_sequence[0, -1] = new_feature_scaled[0]

                # ============================================
                # Generate Graph with Future Predictions
                # ============================================
                plt.figure(figsize=(16, 8))

                # Plot historical actual delays
                actual_dep_delays = [t[0] for t in targets]
                actual_arr_delays = [t[1] for t in targets]
                historical_dates = [d.strftime('%m/%d') for d in dates]

                # Plot last 20 historical points
                plot_range = min(20, len(historical_dates))
                plt.plot(historical_dates[-plot_range:], actual_dep_delays[-plot_range:],
                         'b-o', label='Historical Departure Delay', linewidth=2, markersize=6)
                plt.plot(historical_dates[-plot_range:], actual_arr_delays[-plot_range:],
                         'g-s', label='Historical Arrival Delay', linewidth=2, markersize=6)

                # Plot future predictions
                if future_predictions:
                    future_dates = [p['date'].strftime('%m/%d') for p in future_predictions]
                    future_dep_delays = [p['pred_dep_delay'] for p in future_predictions]
                    future_arr_delays = [p['pred_arr_delay'] for p in future_predictions]

                    # Add a vertical line separating historical from future
                    if historical_dates:
                        plt.axvline(x=len(historical_dates) - 1, color='red', linestyle='--', linewidth=2, alpha=0.7)
                        plt.text(len(historical_dates) - 1,
                                 max(actual_dep_delays[-plot_range:] + actual_arr_delays[-plot_range:] + [30]),
                                 '  FUTURE →', color='red', fontsize=12, fontweight='bold')

                    plt.plot(future_dates, future_dep_delays, 'b--o',
                             label='Predicted Departure Delay (Future)', linewidth=2.5,
                             markersize=8, markerfacecolor='white', markeredgewidth=2)
                    plt.plot(future_dates, future_arr_delays, 'g--s',
                             label='Predicted Arrival Delay (Future)', linewidth=2.5,
                             markersize=8, markerfacecolor='white', markeredgewidth=2)

                plt.xlabel('Flight Date', fontsize=12)
                plt.ylabel('Delay (minutes)', fontsize=12)
                plt.title(
                    f'Flight Delay Prediction - {flight.Flight_Name} ({flight.Source} → {flight.Destination})\nHistorical + Next 7 Days Forecast',
                    fontsize=14, fontweight='bold')
                plt.legend(loc='upper left', fontsize=10, framealpha=0.9)
                plt.grid(True, alpha=0.3, linestyle='--')
                plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)
                plt.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
                plt.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)
                plt.xticks(rotation=45)
                plt.tight_layout()

                buffer = io.BytesIO()
                plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()
                plt.close()

                graph = base64.b64encode(image_png).decode('utf-8')

        # Calculate statistics
        if targets:
            dep_delays = [t[0] for t in targets]
            arr_delays = [t[1] for t in targets]
            avg_dep_delay = np.mean(dep_delays)
            avg_arr_delay = np.mean(arr_delays)
            on_time_count = len([t for t in targets if t[0] <= 15 and t[1] <= 15])
            on_time_percentage = (on_time_count / len(targets)) * 100 if targets else 0
            max_delay = max(max(dep_delays) if dep_delays else 0, max(arr_delays) if arr_delays else 0)
        else:
            avg_dep_delay = avg_arr_delay = on_time_percentage = max_delay = 0

        context = {
            'flight': flight,
            'graph': graph,
            'historical_predictions': historical_predictions,
            'future_predictions': future_predictions,
            'has_model': has_model,
            'total_records': len(features),
            'avg_dep_delay': round(avg_dep_delay, 2),
            'avg_arr_delay': round(avg_arr_delay, 2),
            'on_time_percentage': round(on_time_percentage, 1),
            'max_delay': round(max_delay, 2),
            'today': date.today(),
        }

        return render(request, 'Airline operator/delay_prediction.html', context)

    except Flight.DoesNotExist:
        messages.error(request, "Flight not found")
        return redirect('/myapp/viewflights/')
    except Exception as e:
        messages.error(request, f"Error in prediction: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect('/myapp/viewflights/')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Avg, Q
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import io
import base64
import os
import calendar
from .models import Flight, Flight_Schedule, Flight_LandingdepTime


def delay_trend_analysis(request, flight_id):
    try:
        # Get flight details
        flight = Flight.objects.get(id=flight_id)

        # Get all schedules for this flight ordered by date
        schedules = Flight_Schedule.objects.filter(FLIGHT=flight).order_by('Flight_Date')

        if not schedules.exists():
            messages.error(request, "No flight schedules found for this flight")
            return redirect('/myapp/viewflights/')

        # Helper function to convert time string to minutes
        def time_to_minutes(time_str):
            try:
                if len(str(time_str).split(':')) == 3:
                    t = datetime.strptime(str(time_str), '%H:%M:%S').time()
                else:
                    t = datetime.strptime(str(time_str), '%H:%M').time()
                return t.hour * 60 + t.minute
            except:
                return 0

        # Collect data for analysis
        dates = []
        dep_delays = []
        arr_delays = []
        weekdays = []
        months = []
        hours = []
        flight_numbers = []

        for schedule in schedules:
            actual_times = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

            if actual_times:
                scheduled_dep = time_to_minutes(schedule.Scheduled_Departure)
                scheduled_arr = time_to_minutes(schedule.Scheduled_Arrival)
                actual_dep = time_to_minutes(actual_times.departtime)
                actual_arr = time_to_minutes(actual_times.arrivaltime)

                dep_delay = actual_dep - scheduled_dep
                arr_delay = actual_arr - scheduled_arr

                dep_delays.append(dep_delay)
                arr_delays.append(arr_delay)
                dates.append(schedule.Flight_Date)
                weekdays.append(schedule.Flight_Date.weekday())
                months.append(schedule.Flight_Date.month)
                hours.append(scheduled_dep // 60)  # Hour of scheduled departure
                flight_numbers.append(schedule.id)

        if not dep_delays:
            messages.error(request, "No delay data available for this flight")
            return redirect('/myapp/viewflights/')

        # ============================================
        # GRAPH 1: Overall Delay Trend Over Time
        # ============================================
        plt.figure(figsize=(14, 6))

        # Calculate moving average for trend line
        window = min(7, len(dep_delays))
        if window > 1:
            dep_ma = np.convolve(dep_delays, np.ones(window) / window, mode='valid')
            arr_ma = np.convolve(arr_delays, np.ones(window) / window, mode='valid')
            ma_dates = dates[window - 1:]

            plt.plot(dates, dep_delays, 'b-', alpha=0.3, label='Daily Departure Delay', linewidth=1, marker='o',
                     markersize=3)
            plt.plot(dates, arr_delays, 'g-', alpha=0.3, label='Daily Arrival Delay', linewidth=1, marker='s',
                     markersize=3)
            plt.plot(ma_dates, dep_ma, 'b-', linewidth=3, label=f'{window}-Day Trend (Departure)')
            plt.plot(ma_dates, arr_ma, 'g-', linewidth=3, label=f'{window}-Day Trend (Arrival)')
        else:
            plt.plot(dates, dep_delays, 'b-o', label='Departure Delay', linewidth=2, markersize=6)
            plt.plot(dates, arr_delays, 'g-s', label='Arrival Delay', linewidth=2, markersize=6)

        # Add average lines
        avg_dep = np.mean(dep_delays)
        avg_arr = np.mean(arr_delays)
        plt.axhline(y=avg_dep, color='blue', linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Avg Dep: {avg_dep:.1f} min')
        plt.axhline(y=avg_arr, color='green', linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Avg Arr: {avg_arr:.1f} min')

        # Add threshold lines
        plt.axhline(y=15, color='orange', linestyle=':', linewidth=1, alpha=0.5, label='Warning (15 min)')
        plt.axhline(y=30, color='red', linestyle=':', linewidth=1, alpha=0.5, label='Critical (30 min)')

        plt.xlabel('Flight Date', fontsize=12)
        plt.ylabel('Delay (minutes)', fontsize=12)
        plt.title(f'Delay Trend Over Time - {flight.Flight_Name}', fontsize=14, fontweight='bold')
        plt.legend(loc='upper left', fontsize=10, bbox_to_anchor=(1, 1))
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        trend_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 2: Delay by Day of Week
        # ============================================
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_avg_dep = []
        day_avg_arr = []
        day_counts = []
        day_std_dep = []
        day_std_arr = []

        for day in range(7):
            day_indices = [i for i, d in enumerate(weekdays) if d == day]
            if day_indices:
                day_dep = [dep_delays[i] for i in day_indices]
                day_arr = [arr_delays[i] for i in day_indices]
                day_avg_dep.append(np.mean(day_dep))
                day_avg_arr.append(np.mean(day_arr))
                day_counts.append(len(day_indices))
                day_std_dep.append(np.std(day_dep))
                day_std_arr.append(np.std(day_arr))
            else:
                day_avg_dep.append(0)
                day_avg_arr.append(0)
                day_counts.append(0)
                day_std_dep.append(0)
                day_std_arr.append(0)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        x = np.arange(len(days))
        width = 0.35

        # Bar chart with error bars
        bars1 = ax1.bar(x - width / 2, day_avg_dep, width, yerr=day_std_dep, capsize=5,
                        label='Departure Delay', color='blue', alpha=0.7, ecolor='darkblue')
        bars2 = ax1.bar(x + width / 2, day_avg_arr, width, yerr=day_std_arr, capsize=5,
                        label='Arrival Delay', color='green', alpha=0.7, ecolor='darkgreen')

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}', ha='center', va='bottom', fontsize=9)
        for bar in bars2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}', ha='center', va='bottom', fontsize=9)

        ax1.set_xlabel('Day of Week', fontsize=12)
        ax1.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax1.set_title('Average Delay by Day of Week (with Standard Deviation)', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(days, rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
        ax1.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)

        # Line chart with fill between for range
        ax2.plot(days, day_avg_dep, 'b-o', linewidth=2, markersize=8, label='Departure Delay')
        ax2.plot(days, day_avg_arr, 'g-s', linewidth=2, markersize=8, label='Arrival Delay')

        # Add confidence bands (avg ± std)
        dep_upper = [avg + std for avg, std in zip(day_avg_dep, day_std_dep)]
        dep_lower = [avg - std for avg, std in zip(day_avg_dep, day_std_dep)]
        arr_upper = [avg + std for avg, std in zip(day_avg_arr, day_std_arr)]
        arr_lower = [avg - std for avg, std in zip(day_avg_arr, day_std_arr)]

        ax2.fill_between(days, dep_lower, dep_upper, alpha=0.2, color='blue')
        ax2.fill_between(days, arr_lower, arr_upper, alpha=0.2, color='green')

        # Add count annotations
        for i, (dep, arr, count) in enumerate(zip(day_avg_dep, day_avg_arr, day_counts)):
            ax2.annotate(f'n={count}', (i, max(dep, arr) + 5), ha='center', fontsize=9,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

        ax2.set_xlabel('Day of Week', fontsize=12)
        ax2.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax2.set_title('Delay Pattern with Variability Range', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(days, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
        ax2.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        weekday_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 3: Delay by Hour of Day
        # ============================================
        hour_ranges = range(0, 24)
        hour_avg_dep = []
        hour_avg_arr = []
        hour_counts = []
        hour_std_dep = []
        hour_std_arr = []

        for hour in hour_ranges:
            hour_indices = [i for i, h in enumerate(hours) if h == hour]
            if hour_indices:
                hour_dep = [dep_delays[i] for i in hour_indices]
                hour_arr = [arr_delays[i] for i in hour_indices]
                hour_avg_dep.append(np.mean(hour_dep))
                hour_avg_arr.append(np.mean(hour_arr))
                hour_counts.append(len(hour_indices))
                hour_std_dep.append(np.std(hour_dep))
                hour_std_arr.append(np.std(hour_arr))
            else:
                hour_avg_dep.append(0)
                hour_avg_arr.append(0)
                hour_counts.append(0)
                hour_std_dep.append(0)
                hour_std_arr.append(0)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        x = np.arange(24)
        width = 0.35

        # Bar chart
        bars1 = ax1.bar(x - width / 2, hour_avg_dep, width, label='Departure Delay',
                        color='blue', alpha=0.7, edgecolor='darkblue')
        bars2 = ax1.bar(x + width / 2, hour_avg_arr, width, label='Arrival Delay',
                        color='green', alpha=0.7, edgecolor='darkgreen')

        # Color code bars based on delay severity
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            if hour_avg_dep[i] > 30:
                bar1.set_color('red')
            elif hour_avg_dep[i] > 15:
                bar1.set_color('orange')

            if hour_avg_arr[i] > 30:
                bar2.set_color('red')
            elif hour_avg_arr[i] > 15:
                bar2.set_color('orange')

        ax1.set_xlabel('Hour of Day (Scheduled Departure)', fontsize=12)
        ax1.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax1.set_title('Average Delay by Hour of Day', fontsize=14, fontweight='bold')
        ax1.set_xticks(x[::2])
        ax1.set_xticklabels([f'{h:02d}:00' for h in x[::2]])
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
        ax1.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)

        # Add frequency heat map in second subplot
        scatter = ax2.scatter(hours, dep_delays, c=dep_delays, cmap='RdYlGn_r',
                              s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
        ax2.set_xlabel('Hour of Day', fontsize=12)
        ax2.set_ylabel('Delay (minutes)', fontsize=12)
        ax2.set_title('Delay Distribution by Hour (Color = Delay Severity)', fontsize=14, fontweight='bold')
        ax2.set_xticks(x[::2])
        ax2.set_xticklabels([f'{h:02d}:00' for h in x[::2]])
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
        ax2.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)

        # Add colorbar
        plt.colorbar(scatter, ax=ax2, label='Delay Minutes')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        hourly_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 4: Monthly Trend Analysis
        # ============================================
        month_names = []
        month_avg_dep = []
        month_avg_arr = []
        month_counts = []

        # Group by month
        unique_months = sorted(set(months))
        for month in unique_months:
            month_indices = [i for i, m in enumerate(months) if m == month]
            month_dep = [dep_delays[i] for i in month_indices]
            month_arr = [arr_delays[i] for i in month_indices]
            month_avg_dep.append(np.mean(month_dep))
            month_avg_arr.append(np.mean(month_arr))
            month_counts.append(len(month_indices))
            month_names.append(calendar.month_name[month])

        plt.figure(figsize=(12, 6))

        x = np.arange(len(month_names))
        width = 0.35

        bars1 = plt.bar(x - width / 2, month_avg_dep, width, label='Departure Delay',
                        color='blue', alpha=0.7)
        bars2 = plt.bar(x + width / 2, month_avg_arr, width, label='Arrival Delay',
                        color='green', alpha=0.7)

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}', ha='center', va='bottom', fontsize=9)
        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height:.1f}', ha='center', va='bottom', fontsize=9)

        # Add count annotations
        for i, count in enumerate(month_counts):
            plt.text(i, max(month_avg_dep[i], month_avg_arr[i]) + 2,
                     f'n={count}', ha='center', fontsize=9, style='italic')

        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Delay (minutes)', fontsize=12)
        plt.title(f'Monthly Delay Trend - {flight.Flight_Name}', fontsize=14, fontweight='bold')
        plt.xticks(x, month_names, rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        plt.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.5)
        plt.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.5)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        monthly_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 5: Delay Distribution (Histogram)
        # ============================================
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Departure delay distribution
        n_dep, bins_dep, patches_dep = ax1.hist(dep_delays, bins=15, color='blue',
                                                alpha=0.7, edgecolor='black', linewidth=1)

        # Color code histogram bars
        for patch, bin_edge in zip(patches_dep, bins_dep[:-1]):
            if bin_edge > 30:
                patch.set_facecolor('red')
            elif bin_edge > 15:
                patch.set_facecolor('orange')
            else:
                patch.set_facecolor('green')

        ax1.axvline(np.mean(dep_delays), color='red', linestyle='--', linewidth=2,
                    label=f'Mean: {np.mean(dep_delays):.1f} min')
        ax1.axvline(np.median(dep_delays), color='blue', linestyle='--', linewidth=2,
                    label=f'Median: {np.median(dep_delays):.1f} min')
        ax1.axvline(0, color='black', linestyle='-', linewidth=1)

        ax1.set_xlabel('Delay (minutes)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Departure Delay Distribution', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Arrival delay distribution
        n_arr, bins_arr, patches_arr = ax2.hist(arr_delays, bins=15, color='green',
                                                alpha=0.7, edgecolor='black', linewidth=1)

        # Color code histogram bars
        for patch, bin_edge in zip(patches_arr, bins_arr[:-1]):
            if bin_edge > 30:
                patch.set_facecolor('red')
            elif bin_edge > 15:
                patch.set_facecolor('orange')
            else:
                patch.set_facecolor('green')

        ax2.axvline(np.mean(arr_delays), color='red', linestyle='--', linewidth=2,
                    label=f'Mean: {np.mean(arr_delays):.1f} min')
        ax2.axvline(np.median(arr_delays), color='green', linestyle='--', linewidth=2,
                    label=f'Median: {np.median(arr_delays):.1f} min')
        ax2.axvline(0, color='black', linestyle='-', linewidth=1)

        ax2.set_xlabel('Delay (minutes)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Arrival Delay Distribution', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        distribution_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 6: Cumulative Delay Analysis
        # ============================================
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Cumulative delay over time
        cumulative_dep = np.cumsum(dep_delays)
        cumulative_arr = np.cumsum(arr_delays)

        ax1.fill_between(dates, 0, cumulative_dep, alpha=0.5, color='blue', label='Departure')
        ax1.fill_between(dates, 0, cumulative_arr, alpha=0.5, color='green', label='Arrival')
        ax1.plot(dates, cumulative_dep, 'b-', linewidth=2)
        ax1.plot(dates, cumulative_arr, 'g-', linewidth=2)

        ax1.set_xlabel('Flight Date', fontsize=12)
        ax1.set_ylabel('Cumulative Delay (minutes)', fontsize=12)
        ax1.set_title('Cumulative Delay Over Time', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax1.axhline(y=500, color='red', linestyle='--', linewidth=1, alpha=0.5, label='_nolegend_')
        ax1.axhline(y=1000, color='darkred', linestyle='--', linewidth=1, alpha=0.5, label='_nolegend_')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

        # Delay severity pie chart
        dep_categories = {
            'Early/Early': len([d for d in dep_delays if d < -5]),
            'On Time (-5 to 5)': len([d for d in dep_delays if -5 <= d <= 5]),
            'Minor (5-15)': len([d for d in dep_delays if 5 < d <= 15]),
            'Moderate (15-30)': len([d for d in dep_delays if 15 < d <= 30]),
            'Severe (>30)': len([d for d in dep_delays if d > 30])
        }

        colors = ['lightgreen', 'green', 'yellow', 'orange', 'red']
        wedges, texts, autotexts = ax2.pie(dep_categories.values(), labels=dep_categories.keys(),
                                           autopct='%1.1f%%', colors=colors, startangle=90)

        # Make percentage text white and bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax2.set_title('Departure Delay Severity Distribution', fontsize=14, fontweight='bold')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        cumulative_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # Calculate comprehensive statistics
        stats = {
            'total_flights': len(dep_delays),
            'avg_dep_delay': np.mean(dep_delays),
            'avg_arr_delay': np.mean(arr_delays),
            'median_dep_delay': np.median(dep_delays),
            'median_arr_delay': np.median(arr_delays),
            'std_dep_delay': np.std(dep_delays),
            'std_arr_delay': np.std(arr_delays),
            'min_dep_delay': np.min(dep_delays),
            'min_arr_delay': np.min(arr_delays),
            'max_dep_delay': np.max(dep_delays),
            'max_arr_delay': np.max(arr_delays),
            'total_dep_delay_minutes': np.sum([d for d in dep_delays if d > 0]),
            'total_arr_delay_minutes': np.sum([d for d in arr_delays if d > 0]),

            # On-time performance
            'on_time_dep': len([d for d in dep_delays if -5 <= d <= 5]),
            'on_time_arr': len([d for d in arr_delays if -5 <= d <= 5]),
            'on_time_both': len([(d, a) for d, a in zip(dep_delays, arr_delays) if -5 <= d <= 5 and -5 <= a <= 5]),

            # Delay categories
            'early_dep': len([d for d in dep_delays if d < -5]),
            'minor_dep': len([d for d in dep_delays if 5 < d <= 15]),
            'moderate_dep': len([d for d in dep_delays if 15 < d <= 30]),
            'severe_dep': len([d for d in dep_delays if d > 30]),

            # Best and worst days
            'best_day_idx': np.argmin(dep_delays),
            'worst_day_idx': np.argmax(dep_delays),

            # Day with most delays
            'worst_weekday': days[np.argmax(day_avg_dep)],
            'best_weekday': days[np.argmin([d for d in day_avg_dep if d > 0] or [0])],

            # Peak hour
            'peak_hour': np.argmax(hour_avg_dep),

            # Trends
            'delay_trend': 'Increasing' if len(dep_delays) > 1 and dep_delays[-1] > dep_delays[
                0] else 'Decreasing' if len(dep_delays) > 1 and dep_delays[-1] < dep_delays[0] else 'Stable',
            'volatility': 'High' if np.std(dep_delays) > 20 else 'Medium' if np.std(dep_delays) > 10 else 'Low'
        }

        stats['on_time_dep_pct'] = (stats['on_time_dep'] / stats['total_flights']) * 100
        stats['on_time_arr_pct'] = (stats['on_time_arr'] / stats['total_flights']) * 100
        stats['on_time_both_pct'] = (stats['on_time_both'] / stats['total_flights']) * 100

        # Create a date range for the table
        context = {
            'flight': flight,
            'trend_graph': trend_graph,
            'weekday_graph': weekday_graph,
            'hourly_graph': hourly_graph,
            'monthly_graph': monthly_graph,
            'distribution_graph': distribution_graph,
            'cumulative_graph': cumulative_graph,
            'stats': stats,
            'dates': dates[-20:],  # Last 20 dates
            'dep_delays': dep_delays[-20:],  # Last 20 departure delays
            'arr_delays': arr_delays[-20:],  # Last 20 arrival delays
            'total_records': len(dep_delays),
            'date_range': range(min(20, len(dates))),  # Range for looping
        }

        return render(request, 'Airline operator/delay_trend_analysis.html', context)

    except Flight.DoesNotExist:
        messages.error(request, "Flight not found")
        return redirect('/myapp/viewflights/')
    except Exception as e:
        messages.error(request, f"Error in analysis: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect('/myapp/viewflights/')


from django.db.models import Avg, Count, Q, StdDev
from django.db.models.functions import TruncMonth, TruncDay, json
from collections import defaultdict


def frequent_delay_routes(request, flight_id):
    try:
        # Get the selected flight
        current_flight = Flight.objects.get(id=flight_id)
        current_route = f"{current_flight.Source} → {current_flight.Destination}"

        # Get all flights with the same source and destination
        same_route_flights = Flight.objects.filter(
            Source=current_flight.Source,
            Destination=current_flight.Destination
        )

        route_data = {
            'route': current_route,
            'source': current_flight.Source,
            'destination': current_flight.Destination,
            'flights': [],
            'total_flights': 0,
            'total_delayed': 0,
            'avg_dep_delay': 0,
            'avg_arr_delay': 0,
            'max_dep_delay': float('-inf'),
            'max_arr_delay': float('-inf'),
            'min_dep_delay': float('inf'),
            'min_arr_delay': float('inf'),
            'delay_frequency': 0,
            'airlines': set(),
            'monthly_delays': defaultdict(list),
            'hourly_delays': defaultdict(list),
            'weekly_delays': defaultdict(list),
            'delay_causes': defaultdict(int),
            'flight_performance': []
        }

        # Helper function to convert time to minutes
        def time_to_minutes(time_str):
            try:
                if len(str(time_str).split(':')) == 3:
                    t = datetime.strptime(str(time_str), '%H:%M:%S').time()
                else:
                    t = datetime.strptime(str(time_str), '%H:%M').time()
                return t.hour * 60 + t.minute
            except:
                return 0

        # Collect data for all flights on this route
        all_dep_delays = []
        all_arr_delays = []

        for flight in same_route_flights:
            flight_schedules = Flight_Schedule.objects.filter(FLIGHT=flight).order_by('-Flight_Date')
            flight_delays = []

            for schedule in flight_schedules:
                actual = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

                if actual:
                    scheduled_dep = time_to_minutes(schedule.Scheduled_Departure)
                    scheduled_arr = time_to_minutes(schedule.Scheduled_Arrival)
                    actual_dep = time_to_minutes(actual.departtime)
                    actual_arr = time_to_minutes(actual.arrivaltime)

                    dep_delay = actual_dep - scheduled_dep
                    arr_delay = actual_arr - scheduled_arr

                    all_dep_delays.append(dep_delay)
                    all_arr_delays.append(arr_delay)

                    # Store flight performance data
                    flight_delays.append({
                        'date': schedule.Flight_Date,
                        'scheduled_dep': schedule.Scheduled_Departure,
                        'scheduled_arr': schedule.Scheduled_Arrival,
                        'actual_dep': actual.departtime,
                        'actual_arr': actual.arrivaltime,
                        'dep_delay': dep_delay,
                        'arr_delay': arr_delay
                    })

                    # Update route data
                    route_data['total_flights'] += 1
                    route_data['avg_dep_delay'] += dep_delay
                    route_data['avg_arr_delay'] += arr_delay

                    if dep_delay > 0:
                        route_data['total_delayed'] += 1

                    route_data['max_dep_delay'] = max(route_data['max_dep_delay'], dep_delay)
                    route_data['max_arr_delay'] = max(route_data['max_arr_delay'], arr_delay)
                    route_data['min_dep_delay'] = min(route_data['min_dep_delay'], dep_delay)
                    route_data['min_arr_delay'] = min(route_data['min_arr_delay'], arr_delay)

                    route_data['airlines'].add(flight.Flight_Name.split('-')[0].strip())

                    # Monthly breakdown
                    month_key = schedule.Flight_Date.strftime('%Y-%m')
                    route_data['monthly_delays'][month_key].append(dep_delay)

                    # Hourly breakdown
                    hour_key = scheduled_dep // 60
                    route_data['hourly_delays'][hour_key].append(dep_delay)

                    # Weekly breakdown
                    weekday = schedule.Flight_Date.strftime('%A')
                    route_data['weekly_delays'][weekday].append(dep_delay)

                    # Determine likely cause of delay
                    if dep_delay > 30:
                        if scheduled_dep // 60 in [17, 18, 19, 20]:  # Evening peak
                            route_data['delay_causes']['Evening Peak Traffic'] += 1
                        elif schedule.Flight_Date.weekday() in [4, 5]:  # Friday, Saturday
                            route_data['delay_causes']['Weekend Rush'] += 1
                        else:
                            route_data['delay_causes']['Operational Issues'] += 1
                    elif dep_delay > 15:
                        route_data['delay_causes']['Moderate Congestion'] += 1
                    elif dep_delay > 5:
                        route_data['delay_causes']['Minor Delays'] += 1

            # Store flight summary
            if flight_delays:
                route_data['flight_performance'].append({
                    'flight_name': flight.Flight_Name,
                    'flight_id': flight.id,
                    'total_flights': len(flight_delays),
                    'avg_delay': np.mean([d['dep_delay'] for d in flight_delays]),
                    'delay_frequency': len([d for d in flight_delays if d['dep_delay'] > 0]) / len(flight_delays) * 100,
                    'recent_delays': flight_delays[:5]  # Last 5 flights
                })

        # Calculate averages and percentages
        if route_data['total_flights'] > 0:
            route_data['avg_dep_delay'] = route_data['avg_dep_delay'] / route_data['total_flights']
            route_data['avg_arr_delay'] = route_data['avg_arr_delay'] / route_data['total_flights']
            route_data['delay_frequency'] = (route_data['total_delayed'] / route_data['total_flights']) * 100
            route_data['airlines'] = list(route_data['airlines'])

            # Calculate reliability score (lower is better)
            route_data['reliability_score'] = (
                route_data['avg_dep_delay'] * 0.4 +
                route_data['avg_arr_delay'] * 0.3 +
                (100 - route_data['delay_frequency']) * 0.3
            )

            # Sort flight performance by delay frequency
            route_data['flight_performance'].sort(key=lambda x: x['delay_frequency'], reverse=True)

        # ============================================
        # GRAPH 1: Delay Comparison Across Airlines
        # ============================================
        plt.figure(figsize=(14, 6))

        flight_names = [f['flight_name'] for f in route_data['flight_performance']]
        flight_delays = [f['avg_delay'] for f in route_data['flight_performance']]
        flight_freq = [f['delay_frequency'] for f in route_data['flight_performance']]

        x = np.arange(len(flight_names))
        width = 0.35

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Bar chart for average delay
        bars1 = ax1.bar(x, flight_delays, width, color='blue', alpha=0.7)
        ax1.set_xlabel('Flight', fontsize=12)
        ax1.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax1.set_title(f'Average Delay by Flight - {current_route}', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(flight_names, rotation=45, ha='right')
        ax1.axhline(y=route_data['avg_dep_delay'], color='red', linestyle='--', linewidth=2,
                    label=f'Route Avg: {route_data["avg_dep_delay"]:.1f} min')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Highlight current flight
        for i, name in enumerate(flight_names):
            if current_flight.Flight_Name in name:
                bars1[i].set_color('red')
                bars1[i].set_alpha(0.9)

        # Bar chart for delay frequency
        bars2 = ax2.bar(x, flight_freq, width, color='green', alpha=0.7)
        ax2.set_xlabel('Flight', fontsize=12)
        ax2.set_ylabel('Delay Frequency (%)', fontsize=12)
        ax2.set_title(f'Delay Frequency by Flight - {current_route}', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(flight_names, rotation=45, ha='right')
        ax2.axhline(y=route_data['delay_frequency'], color='red', linestyle='--', linewidth=2,
                    label=f'Route Avg: {route_data["delay_frequency"]:.1f}%')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        # Highlight current flight
        for i, name in enumerate(flight_names):
            if current_flight.Flight_Name in name:
                bars2[i].set_color('red')
                bars2[i].set_alpha(0.9)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        flight_comparison_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 2: Time of Day Delay Pattern
        # ============================================
        plt.figure(figsize=(14, 6))

        hours = sorted(route_data['hourly_delays'].keys())
        hourly_avgs = [np.mean(route_data['hourly_delays'][h]) for h in hours]
        hourly_counts = [len(route_data['hourly_delays'][h]) for h in hours]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Line chart for hourly pattern
        ax1.plot(hours, hourly_avgs, 'b-o', linewidth=2, markersize=8)
        ax1.fill_between(hours, hourly_avgs, alpha=0.3, color='blue')
        ax1.set_xlabel('Hour of Day', fontsize=12)
        ax1.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax1.set_title(f'Hourly Delay Pattern - {current_route}', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(0, 24, 2))
        ax1.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
        ax1.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Warning')
        ax1.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Critical')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Bar chart for flight frequency by hour
        ax2.bar(hours, hourly_counts, color='green', alpha=0.7)
        ax2.set_xlabel('Hour of Day', fontsize=12)
        ax2.set_ylabel('Number of Flights', fontsize=12)
        ax2.set_title('Flight Distribution by Hour', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(0, 24, 2))
        ax2.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        hourly_pattern_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 3: Weekly Pattern
        # ============================================
        plt.figure(figsize=(12, 6))

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_avgs = []
        weekly_counts = []

        for day in days:
            if day in route_data['weekly_delays'] and route_data['weekly_delays'][day]:
                weekly_avgs.append(np.mean(route_data['weekly_delays'][day]))
                weekly_counts.append(len(route_data['weekly_delays'][day]))
            else:
                weekly_avgs.append(0)
                weekly_counts.append(0)

        x = np.arange(len(days))
        width = 0.35

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Bar chart for weekly pattern
        bars = ax1.bar(x, weekly_avgs, width,
                       color=['red' if d > 15 else 'orange' if d > 5 else 'green' for d in weekly_avgs])
        ax1.set_xlabel('Day of Week', fontsize=12)
        ax1.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax1.set_title(f'Weekly Delay Pattern - {current_route}', fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(days, rotation=45)
        ax1.axhline(y=route_data['avg_dep_delay'], color='blue', linestyle='--', linewidth=2,
                    label=f'Overall Avg: {route_data["avg_dep_delay"]:.1f} min')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar, val in zip(bars, weekly_avgs):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{val:.1f}', ha='center', va='bottom', fontsize=9)

        # Line chart for trend
        ax2.plot(days, weekly_avgs, 'ro-', linewidth=2, markersize=8)
        ax2.fill_between(days, weekly_avgs, alpha=0.3, color='red')
        ax2.set_xlabel('Day of Week', fontsize=12)
        ax2.set_ylabel('Average Delay (minutes)', fontsize=12)
        ax2.set_title('Weekly Delay Trend', fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(days, rotation=45)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        weekly_pattern_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 4: Delay Distribution
        # ============================================
        plt.figure(figsize=(14, 6))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Histogram
        n_dep, bins_dep, patches_dep = ax1.hist(all_dep_delays, bins=15, color='blue',
                                                alpha=0.7, edgecolor='black', linewidth=1)

        # Color code histogram bars
        for patch, bin_edge in zip(patches_dep, bins_dep[:-1]):
            if bin_edge > 30:
                patch.set_facecolor('red')
            elif bin_edge > 15:
                patch.set_facecolor('orange')
            else:
                patch.set_facecolor('green')

        ax1.axvline(route_data['avg_dep_delay'], color='red', linestyle='--', linewidth=2,
                    label=f'Mean: {route_data["avg_dep_delay"]:.1f} min')
        ax1.axvline(0, color='black', linestyle='-', linewidth=1)
        ax1.set_xlabel('Delay (minutes)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Delay Distribution', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Pie chart for delay categories
        categories = {
            'Early (<0)': len([d for d in all_dep_delays if d < 0]),
            'On Time (0-15)': len([d for d in all_dep_delays if 0 <= d <= 15]),
            'Moderate (15-30)': len([d for d in all_dep_delays if 15 < d <= 30]),
            'Severe (>30)': len([d for d in all_dep_delays if d > 30])
        }

        colors = ['lightgreen', 'green', 'orange', 'red']
        wedges, texts, autotexts = ax2.pie(categories.values(), labels=categories.keys(),
                                           autopct='%1.1f%%', colors=colors, startangle=90)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax2.set_title('Delay Severity Distribution', fontsize=14, fontweight='bold')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        distribution_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 5: Monthly Trend
        # ============================================
        plt.figure(figsize=(14, 6))

        months = sorted(route_data['monthly_delays'].keys())[-12:]  # Last 12 months
        monthly_avgs = [np.mean(route_data['monthly_delays'][m]) for m in months]
        month_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months]

        plt.plot(month_labels, monthly_avgs, 'b-o', linewidth=2, markersize=8)
        plt.fill_between(month_labels, monthly_avgs, alpha=0.3, color='blue')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Delay (minutes)', fontsize=12)
        plt.title(f'Monthly Delay Trend - {current_route}', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=route_data['avg_dep_delay'], color='red', linestyle='--', linewidth=2,
                    label=f'Overall Avg: {route_data["avg_dep_delay"]:.1f} min')
        plt.legend()

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        monthly_trend_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # Prepare context
        context = {
            'current_flight': current_flight,
            'route': current_route,
            'source': current_flight.Source,
            'destination': current_flight.Destination,
            'route_data': route_data,
            'flight_comparison_graph': flight_comparison_graph,
            'hourly_pattern_graph': hourly_pattern_graph,
            'weekly_pattern_graph': weekly_pattern_graph,
            'distribution_graph': distribution_graph,
            'monthly_trend_graph': monthly_trend_graph,
            'total_airlines': len(route_data['airlines']),
            'total_flights_route': route_data['total_flights'],
            'avg_delay_route': round(route_data['avg_dep_delay'], 1),
            'delay_frequency_route': round(route_data['delay_frequency'], 1),
            'peak_hour': max(route_data['hourly_delays'].items(), key=lambda x: np.mean(x[1]))[0] if route_data[
                'hourly_delays'] else 'N/A',
            'worst_day': max(route_data['weekly_delays'].items(), key=lambda x: np.mean(x[1]))[0] if route_data[
                'weekly_delays'] else 'N/A',
        }

        return render(request, 'Airline operator/frequent_delay_routes.html', context)

    except Flight.DoesNotExist:
        messages.error(request, "Flight not found")
        return redirect('/myapp/viewflights/')
    except Exception as e:
        messages.error(request, f"Error analyzing routes: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect('/myapp/viewflights/')


from django.shortcuts import render, redirect
from django.contrib import messages
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64
from collections import defaultdict
from .models import Flight, Flight_Schedule, Flight_LandingdepTime


def monitor_delays(request, flight_id):
    try:
        # Get flight details
        flight = Flight.objects.get(id=flight_id)

        # Get all schedules for this flight
        schedules = Flight_Schedule.objects.filter(FLIGHT=flight).order_by('Flight_Date')

        if not schedules.exists():
            messages.error(request, "No flight schedules found")
            return redirect('/myapp/view_flights_autho/')

        # Helper function to convert time to minutes
        def time_to_minutes(time_str):
            try:
                if len(str(time_str).split(':')) == 3:
                    t = datetime.strptime(str(time_str), '%H:%M:%S').time()
                else:
                    t = datetime.strptime(str(time_str), '%H:%M').time()
                return t.hour * 60 + t.minute
            except:
                return 0

        # Collect monitoring data
        dates = []
        dep_delays = []
        arr_delays = []
        dep_hours = []  # For peak hour analysis
        arr_hours = []  # For peak hour analysis
        weekdays = []  # For peak day analysis

        for schedule in schedules:
            actual = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

            if actual:
                scheduled_dep = time_to_minutes(schedule.Scheduled_Departure)
                scheduled_arr = time_to_minutes(schedule.Scheduled_Arrival)
                actual_dep = time_to_minutes(actual.departtime)
                actual_arr = time_to_minutes(actual.arrivaltime)

                dep_delay = actual_dep - scheduled_dep
                arr_delay = actual_arr - scheduled_arr

                dates.append(schedule.Flight_Date)
                dep_delays.append(dep_delay)
                arr_delays.append(arr_delay)
                dep_hours.append(scheduled_dep // 60)  # Hour of departure
                arr_hours.append(scheduled_arr // 60)  # Hour of arrival
                weekdays.append(schedule.Flight_Date.weekday())  # Day of week (0=Monday)

        if not dep_delays:
            messages.error(request, "No delay data available")
            return redirect('/myapp/view_flights_autho/')

        # ============================================
        # GRAPH 1: Departure vs Arrival Delays Over Time
        # ============================================
        plt.figure(figsize=(16, 8))

        # Use last 30 flights or all if less
        if len(dates) > 30:
            plot_dates = dates[-30:]
            plot_dep_delays = dep_delays[-30:]
            plot_arr_delays = arr_delays[-30:]
            title_suffix = "Last 30 Flights"
        else:
            plot_dates = dates
            plot_dep_delays = dep_delays
            plot_arr_delays = arr_delays
            title_suffix = f"All {len(dates)} Flights"

        date_labels = [d.strftime('%d %b') for d in plot_dates]

        # Create the plot
        fig, ax = plt.subplots(figsize=(16, 8))

        # Plot departure delays
        ax.plot(date_labels, plot_dep_delays, 'b-o', linewidth=2.5, markersize=8,
                label='Departure Delay', markerfacecolor='white', markeredgewidth=2)

        # Plot arrival delays
        ax.plot(date_labels, plot_arr_delays, 'r-s', linewidth=2.5, markersize=8,
                label='Arrival Delay', markerfacecolor='white', markeredgewidth=2)

        # Fill between the lines
        ax.fill_between(date_labels, plot_dep_delays, plot_arr_delays, alpha=0.2, color='gray')

        # Add threshold lines
        ax.axhline(y=15, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='Warning (15 min)')
        ax.axhline(y=30, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Critical (30 min)')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

        # Add average lines
        avg_dep = np.mean(dep_delays)
        avg_arr = np.mean(arr_delays)
        ax.axhline(y=avg_dep, color='blue', linestyle=':', linewidth=2, alpha=0.7,
                   label=f'Avg Dep: {avg_dep:.1f} min')
        ax.axhline(y=avg_arr, color='red', linestyle=':', linewidth=2, alpha=0.7,
                   label=f'Avg Arr: {avg_arr:.1f} min')

        # Highlight max points
        max_dep_idx = np.argmax(plot_dep_delays)
        max_arr_idx = np.argmax(plot_arr_delays)

        ax.plot(max_dep_idx, plot_dep_delays[max_dep_idx], 'b*', markersize=15,
                label=f'Max Dep: {plot_dep_delays[max_dep_idx]:.0f} min')
        ax.plot(max_arr_idx, plot_arr_delays[max_arr_idx], 'r*', markersize=15,
                label=f'Max Arr: {plot_arr_delays[max_arr_idx]:.0f} min')

        # Customize the plot
        ax.set_xlabel('Flight Date', fontsize=14, fontweight='bold')
        ax.set_ylabel('Delay (minutes)', fontsize=14, fontweight='bold')
        ax.set_title(
            f'Departure vs Arrival Delay Monitor - {flight.Flight_Name} ({flight.Source} → {flight.Destination})\n{title_suffix}',
            fontsize=16, fontweight='bold', pad=20)

        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')

        # Add legend
        ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

        # Add grid
        ax.grid(True, alpha=0.3, linestyle='--')

        # Set y-axis limits with some padding
        min_val = min(min(plot_dep_delays), min(plot_arr_delays), 0)
        max_val = max(max(plot_dep_delays), max(plot_arr_delays), 30)
        ax.set_ylim(min_val - 5, max_val + 10)

        # Add value labels on key points (every 5th point to avoid clutter)
        for i in range(0, len(date_labels), 5):
            if i < len(plot_dep_delays):
                ax.annotate(f'{plot_dep_delays[i]:.0f}',
                            (i, plot_dep_delays[i]),
                            textcoords="offset points",
                            xytext=(0, 10),
                            ha='center',
                            fontsize=9,
                            bbox=dict(boxstyle='round,pad=0.2', facecolor='blue', alpha=0.1))

            if i < len(plot_arr_delays):
                ax.annotate(f'{plot_arr_delays[i]:.0f}',
                            (i, plot_arr_delays[i]),
                            textcoords="offset points",
                            xytext=(0, -15),
                            ha='center',
                            fontsize=9,
                            bbox=dict(boxstyle='round,pad=0.2', facecolor='red', alpha=0.1))

        plt.tight_layout()

        # Convert plot to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        delay_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 2: Peak Delay Hours (Departure)
        # ============================================
        plt.figure(figsize=(12, 6))

        # Group delays by hour
        hour_dep_delays = defaultdict(list)
        hour_arr_delays = defaultdict(list)

        for hour, dep_delay, arr_delay in zip(dep_hours, dep_delays, arr_delays):
            hour_dep_delays[hour].append(dep_delay)
            hour_arr_delays[hour].append(arr_delay)

        # Calculate average delay per hour
        hours_range = range(24)
        avg_dep_by_hour = []
        avg_arr_by_hour = []
        count_by_hour = []

        for hour in hours_range:
            if hour in hour_dep_delays:
                avg_dep_by_hour.append(np.mean(hour_dep_delays[hour]))
                avg_arr_by_hour.append(np.mean(hour_arr_delays[hour]))
                count_by_hour.append(len(hour_dep_delays[hour]))
            else:
                avg_dep_by_hour.append(0)
                avg_arr_by_hour.append(0)
                count_by_hour.append(0)

        # Find peak hours
        peak_dep_hour = np.argmax(avg_dep_by_hour)
        peak_arr_hour = np.argmax(avg_arr_by_hour)
        peak_dep_delay = avg_dep_by_hour[peak_dep_hour]
        peak_arr_delay = avg_arr_by_hour[peak_arr_hour]

        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Bar chart for departure delays by hour
        colors_dep = ['red' if h == peak_dep_hour else 'orange' if avg_dep_by_hour[h] > 15 else 'blue' for h in
                      hours_range]
        bars1 = ax1.bar(hours_range, avg_dep_by_hour, color=colors_dep, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Hour of Day (Departure Time)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Average Departure Delay (minutes)', fontsize=12, fontweight='bold')
        ax1.set_title(f'Peak Departure Delay Hours - {flight.Flight_Name}', fontsize=14, fontweight='bold')
        ax1.set_xticks(range(0, 24, 2))
        ax1.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
        ax1.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Warning')
        ax1.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Critical')
        ax1.grid(True, alpha=0.3, axis='y')

        # Highlight peak hour
        ax1.text(peak_dep_hour, peak_dep_delay + 1, f'PEAK: {peak_dep_delay:.0f} min',
                 ha='center', fontsize=10, fontweight='bold', color='red')

        # Add count labels
        for i, (bar, count) in enumerate(zip(bars1, count_by_hour)):
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width() / 2., 1, f'n={count}',
                         ha='center', va='bottom', fontsize=8, rotation=90)

        # Bar chart for arrival delays by hour
        colors_arr = ['red' if h == peak_arr_hour else 'orange' if avg_arr_by_hour[h] > 15 else 'green' for h in
                      hours_range]
        bars2 = ax2.bar(hours_range, avg_arr_by_hour, color=colors_arr, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Hour of Day (Arrival Time)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average Arrival Delay (minutes)', fontsize=12, fontweight='bold')
        ax2.set_title(f'Peak Arrival Delay Hours - {flight.Flight_Name}', fontsize=14, fontweight='bold')
        ax2.set_xticks(range(0, 24, 2))
        ax2.set_xticklabels([f'{h:02d}:00' for h in range(0, 24, 2)])
        ax2.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Warning')
        ax2.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Critical')
        ax2.grid(True, alpha=0.3, axis='y')

        # Highlight peak hour
        ax2.text(peak_arr_hour, peak_arr_delay + 1, f'PEAK: {peak_arr_delay:.0f} min',
                 ha='center', fontsize=10, fontweight='bold', color='red')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        peak_hours_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 3: Peak Delay Days
        # ============================================
        plt.figure(figsize=(12, 6))

        # Group delays by day of week
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_dep_delays = defaultdict(list)
        day_arr_delays = defaultdict(list)

        for day, dep_delay, arr_delay in zip(weekdays, dep_delays, arr_delays):
            day_dep_delays[day].append(dep_delay)
            day_arr_delays[day].append(arr_delay)

        # Calculate average delay per day
        avg_dep_by_day = []
        avg_arr_by_day = []
        day_counts = []

        for day in range(7):
            if day in day_dep_delays:
                avg_dep_by_day.append(np.mean(day_dep_delays[day]))
                avg_arr_by_day.append(np.mean(day_arr_delays[day]))
                day_counts.append(len(day_dep_delays[day]))
            else:
                avg_dep_by_day.append(0)
                avg_arr_by_day.append(0)
                day_counts.append(0)

        # Find peak days
        peak_dep_day = np.argmax(avg_dep_by_day)
        peak_arr_day = np.argmax(avg_arr_by_day)

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))

        x = np.arange(len(day_names))
        width = 0.35

        # Departure delays bars
        bars1 = ax.bar(x - width / 2, avg_dep_by_day, width, label='Departure Delay',
                       color='blue', alpha=0.7, edgecolor='black')

        # Arrival delays bars
        bars2 = ax.bar(x + width / 2, avg_arr_by_day, width, label='Arrival Delay',
                       color='red', alpha=0.7, edgecolor='black')

        # Highlight peak days
        bars1[peak_dep_day].set_color('darkblue')
        bars1[peak_dep_day].set_alpha(1.0)
        bars2[peak_arr_day].set_color('darkred')
        bars2[peak_arr_day].set_alpha(1.0)

        ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Delay (minutes)', fontsize=12, fontweight='bold')
        ax.set_title(f'Peak Delay Days - {flight.Flight_Name}', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(day_names)
        ax.axhline(y=15, color='orange', linestyle='--', linewidth=1, alpha=0.7, label='Warning')
        ax.axhline(y=30, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Critical')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            height1 = bar1.get_height()
            height2 = bar2.get_height()
            if height1 > 0:
                ax.text(bar1.get_x() + bar1.get_width() / 2., height1 + 0.5,
                        f'{height1:.0f}', ha='center', va='bottom', fontsize=9)
            if height2 > 0:
                ax.text(bar2.get_x() + bar2.get_width() / 2., height2 + 0.5,
                        f'{height2:.0f}', ha='center', va='bottom', fontsize=9)

        # Add count labels
        for i, count in enumerate(day_counts):
            ax.text(i, -3, f'n={count}', ha='center', fontsize=8, color='gray')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        peak_days_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # Calculate statistics
        stats = {
            'total_flights': len(dep_delays),
            'avg_dep_delay': np.mean(dep_delays),
            'avg_arr_delay': np.mean(arr_delays),
            'max_dep_delay': max(dep_delays),
            'max_arr_delay': max(arr_delays),
            'min_dep_delay': min(dep_delays),
            'min_arr_delay': min(arr_delays),
            'on_time_dep': len([d for d in dep_delays if d <= 5]),
            'on_time_arr': len([d for d in arr_delays if d <= 5]),
            'minor_dep': len([d for d in dep_delays if 5 < d <= 15]),
            'minor_arr': len([d for d in arr_delays if 5 < d <= 15]),
            'moderate_dep': len([d for d in dep_delays if 15 < d <= 30]),
            'moderate_arr': len([d for d in arr_delays if 15 < d <= 30]),
            'severe_dep': len([d for d in dep_delays if d > 30]),
            'severe_arr': len([d for d in arr_delays if d > 30]),
            'peak_dep_hour': f"{peak_dep_hour:02d}:00",
            'peak_dep_delay': peak_dep_delay,
            'peak_arr_hour': f"{peak_arr_hour:02d}:00",
            'peak_arr_delay': peak_arr_delay,
            'peak_dep_day': day_names[peak_dep_day],
            'peak_arr_day': day_names[peak_arr_day],
        }

        stats['on_time_pct_dep'] = (stats['on_time_dep'] / stats['total_flights']) * 100
        stats['on_time_pct_arr'] = (stats['on_time_arr'] / stats['total_flights']) * 100

        # Prepare recent flights for table
        recent_flights = []
        for i in range(min(10, len(dates))):
            idx = -1 - i
            recent_flights.append({
                'date': dates[idx],
                'dep_delay': dep_delays[idx],
                'arr_delay': arr_delays[idx],
                'dep_hour': dep_hours[idx],
                'arr_hour': arr_hours[idx],
                'day': day_names[weekdays[idx]],
                'status': 'Severe' if dep_delays[idx] > 30 else 'Moderate' if dep_delays[idx] > 15 else 'Minor' if
                dep_delays[idx] > 5 else 'On Time'
            })

        context = {
            'flight': flight,
            'delay_graph': delay_graph,
            'peak_hours_graph': peak_hours_graph,
            'peak_days_graph': peak_days_graph,
            'stats': stats,
            'recent_flights': recent_flights,
            'peak_dep_hour': f"{stats['peak_dep_hour']} ({stats['peak_dep_delay']:.0f} min avg)",
            'peak_arr_hour': f"{stats['peak_arr_hour']} ({stats['peak_arr_delay']:.0f} min avg)",
            'peak_dep_day': f"{stats['peak_dep_day']} ({avg_dep_by_day[peak_dep_day]:.0f} min avg)",
            'peak_arr_day': f"{stats['peak_arr_day']} ({avg_arr_by_day[peak_arr_day]:.0f} min avg)",
        }

        return render(request, 'authority/monitorarrivaldepdelay.html', context)

    except Flight.DoesNotExist:
        messages.error(request, "Flight not found")
        return redirect('/myapp/view_flights_autho/')
    except Exception as e:
        messages.error(request, f"Error in monitoring: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect('/myapp/view_flights_autho/')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q, Sum
from collections import defaultdict
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time
import io
import base64
import calendar
from .models import Flight, Flight_Schedule, Flight_LandingdepTime


def airport_congestion(request):
    try:
        # Get all flights with their schedules and actual times
        all_flights = Flight.objects.all().select_related()

        if not all_flights.exists():
            messages.error(request, "No flight data available")
            return redirect('/myapp/authorityhome/')

        # Helper function to convert time to minutes
        def time_to_minutes(time_str):
            try:
                if len(str(time_str).split(':')) == 3:
                    t = datetime.strptime(str(time_str), '%H:%M:%S').time()
                else:
                    t = datetime.strptime(str(time_str), '%H:%M').time()
                return t.hour * 60 + t.minute
            except:
                return 0

        # Overall airport statistics
        all_airports = set()
        airport_stats = {}

        # Initialize stats for each airport
        for flight in all_flights:
            all_airports.add(flight.Source)
            all_airports.add(flight.Destination)

        for airport in all_airports:
            airport_stats[airport] = {
                'name': airport,
                'total_departures': 0,
                'total_arrivals': 0,
                'total_flights': 0,
                'total_delayed_dep': 0,
                'total_delayed_arr': 0,
                'sum_dep_delay': 0,
                'sum_arr_delay': 0,
                'severe_dep_delays': 0,
                'severe_arr_delays': 0,
                'hourly_traffic': defaultdict(int),
                'daily_traffic': defaultdict(int),
                'peak_hours': [],
                'airlines': set(),
            }

        # Collect data
        for flight in all_flights:
            schedules = Flight_Schedule.objects.filter(FLIGHT=flight)

            for schedule in schedules:
                actual = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()

                if actual:
                    # Departure airport
                    dep_airport = flight.Source
                    scheduled_dep = time_to_minutes(schedule.Scheduled_Departure)
                    actual_dep = time_to_minutes(actual.departtime)
                    dep_delay = actual_dep - scheduled_dep
                    dep_hour = scheduled_dep // 60
                    dep_weekday = schedule.Flight_Date.weekday()

                    airport_stats[dep_airport]['total_departures'] += 1
                    airport_stats[dep_airport]['total_flights'] += 1
                    airport_stats[dep_airport]['hourly_traffic'][dep_hour] += 1
                    airport_stats[dep_airport]['daily_traffic'][dep_weekday] += 1
                    airport_stats[dep_airport]['airlines'].add(flight.Flight_Name.split('-')[0].strip())

                    if dep_delay > 0:
                        airport_stats[dep_airport]['total_delayed_dep'] += 1
                        airport_stats[dep_airport]['sum_dep_delay'] += dep_delay
                    if dep_delay > 30:
                        airport_stats[dep_airport]['severe_dep_delays'] += 1

                    # Arrival airport
                    arr_airport = flight.Destination
                    scheduled_arr = time_to_minutes(schedule.Scheduled_Arrival)
                    actual_arr = time_to_minutes(actual.arrivaltime)
                    arr_delay = actual_arr - scheduled_arr
                    arr_hour = scheduled_arr // 60
                    arr_weekday = schedule.Flight_Date.weekday()

                    airport_stats[arr_airport]['total_arrivals'] += 1
                    airport_stats[arr_airport]['total_flights'] += 1
                    airport_stats[arr_airport]['hourly_traffic'][arr_hour] += 1
                    airport_stats[arr_airport]['daily_traffic'][arr_weekday] += 1
                    airport_stats[arr_airport]['airlines'].add(flight.Flight_Name.split('-')[0].strip())

                    if arr_delay > 0:
                        airport_stats[arr_airport]['total_delayed_arr'] += 1
                        airport_stats[arr_airport]['sum_arr_delay'] += arr_delay
                    if arr_delay > 30:
                        airport_stats[arr_airport]['severe_arr_delays'] += 1

        # Calculate averages and percentages
        for airport, stats in airport_stats.items():
            # Average delays
            if stats['total_delayed_dep'] > 0:
                stats['avg_dep_delay'] = stats['sum_dep_delay'] / stats['total_delayed_dep']
            else:
                stats['avg_dep_delay'] = 0

            if stats['total_delayed_arr'] > 0:
                stats['avg_arr_delay'] = stats['sum_arr_delay'] / stats['total_delayed_arr']
            else:
                stats['avg_arr_delay'] = 0

            # Delay percentages
            stats['dep_delay_pct'] = (stats['total_delayed_dep'] / stats['total_departures'] * 100) if stats[
                                                                                                           'total_departures'] > 0 else 0
            stats['arr_delay_pct'] = (stats['total_delayed_arr'] / stats['total_arrivals'] * 100) if stats[
                                                                                                         'total_arrivals'] > 0 else 0

            # Severe delay percentages
            stats['severe_dep_pct'] = (stats['severe_dep_delays'] / stats['total_departures'] * 100) if stats[
                                                                                                            'total_departures'] > 0 else 0
            stats['severe_arr_pct'] = (stats['severe_arr_delays'] / stats['total_arrivals'] * 100) if stats[
                                                                                                          'total_arrivals'] > 0 else 0

            # Find peak hours (top 3)
            hourly_items = list(stats['hourly_traffic'].items())
            hourly_items.sort(key=lambda x: x[1], reverse=True)
            stats['peak_hours'] = [(f"{h:02d}:00", count) for h, count in hourly_items[:3]]

            # Find busiest day
            if stats['daily_traffic']:
                busiest_day_idx = max(stats['daily_traffic'], key=stats['daily_traffic'].get)
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                stats['busiest_day'] = days[busiest_day_idx]
            else:
                stats['busiest_day'] = 'N/A'

            # Calculate congestion level
            daily_avg = stats['total_flights'] / 7  # Approximate daily average
            if daily_avg > 50:
                stats['congestion_level'] = 'Very High'
                stats['congestion_color'] = 'danger'
            elif daily_avg > 30:
                stats['congestion_level'] = 'High'
                stats['congestion_color'] = 'warning'
            elif daily_avg > 15:
                stats['congestion_level'] = 'Moderate'
                stats['congestion_color'] = 'info'
            else:
                stats['congestion_level'] = 'Low'
                stats['congestion_color'] = 'success'

            # Calculate overall performance score (simplified)
            delay_factor = 100 - (stats['dep_delay_pct'] * 0.4 + stats['arr_delay_pct'] * 0.4)
            severe_factor = 100 - (stats['severe_dep_pct'] + stats['severe_arr_pct'])
            volume_factor = 100 - (daily_avg * 1.5) if daily_avg * 1.5 < 100 else 0

            stats['performance_score'] = (
                delay_factor * 0.5 +
                severe_factor * 0.3 +
                volume_factor * 0.2
            )
            stats['performance_score'] = max(0, min(100, stats['performance_score']))

            # Performance rating
            if stats['performance_score'] >= 80:
                stats['performance_rating'] = 'Excellent'
                stats['perf_color'] = 'success'
            elif stats['performance_score'] >= 60:
                stats['performance_rating'] = 'Good'
                stats['perf_color'] = 'info'
            elif stats['performance_score'] >= 40:
                stats['performance_rating'] = 'Fair'
                stats['perf_color'] = 'warning'
            else:
                stats['performance_rating'] = 'Poor'
                stats['perf_color'] = 'danger'

            stats['airline_count'] = len(stats['airlines'])

        # Sort airports by total flights
        sorted_airports = sorted(
            airport_stats.items(),
            key=lambda x: x[1]['total_flights'],
            reverse=True
        )

        # ============================================
        # GRAPH 1: Overall Congestion by Hour
        # ============================================
        plt.figure(figsize=(14, 6))

        # Aggregate hourly traffic across all airports
        total_hourly = defaultdict(int)
        for stats in airport_stats.values():
            for hour, count in stats['hourly_traffic'].items():
                total_hourly[hour] += count

        hours = range(24)
        hourly_counts = [total_hourly.get(h, 0) for h in hours]

        plt.bar(hours, hourly_counts, color='steelblue', alpha=0.7, edgecolor='black')
        plt.xlabel('Hour of Day', fontsize=12, fontweight='bold')
        plt.ylabel('Total Flight Volume', fontsize=12, fontweight='bold')
        plt.title('Overall Airport Congestion by Hour', fontsize=14, fontweight='bold')
        plt.xticks(range(0, 24, 2), [f'{h:02d}:00' for h in range(0, 24, 2)])
        plt.grid(True, alpha=0.3, axis='y')

        # Highlight peak hours
        peak_hour = max(range(24), key=lambda x: hourly_counts[x])
        plt.text(peak_hour, hourly_counts[peak_hour] + 5, f'PEAK: {peak_hour:02d}:00',
                 ha='center', fontsize=10, fontweight='bold', color='red')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        hourly_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 2: Overall Congestion by Day
        # ============================================
        plt.figure(figsize=(12, 6))

        # Aggregate daily traffic across all airports
        total_daily = defaultdict(int)
        for stats in airport_stats.values():
            for day, count in stats['daily_traffic'].items():
                total_daily[day] += count

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_counts = [total_daily.get(i, 0) for i in range(7)]

        colors = ['red' if i == 4 else 'orange' if i == 5 else 'steelblue' for i in range(7)]
        plt.bar(days, daily_counts, color=colors, alpha=0.7, edgecolor='black')
        plt.xlabel('Day of Week', fontsize=12, fontweight='bold')
        plt.ylabel('Total Flight Volume', fontsize=12, fontweight='bold')
        plt.title('Overall Airport Congestion by Day', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for i, count in enumerate(daily_counts):
            plt.text(i, count + 5, str(count), ha='center', fontsize=10)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        daily_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 3: Top 10 Busiest Airports
        # ============================================
        plt.figure(figsize=(12, 8))

        top_10 = sorted_airports[:10]
        airports = [a[0][:20] + '...' if len(a[0]) > 20 else a[0] for a in top_10]
        flight_counts = [a[1]['total_flights'] for a in top_10]

        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 10))
        bars = plt.barh(airports, flight_counts, color=colors, alpha=0.8, edgecolor='black')
        plt.xlabel('Total Flights', fontsize=12, fontweight='bold')
        plt.ylabel('Airport', fontsize=12, fontweight='bold')
        plt.title('Top 10 Busiest Airports', fontsize=14, fontweight='bold')

        # Add value labels
        for bar, count in zip(bars, flight_counts):
            plt.text(count + 5, bar.get_y() + bar.get_height() / 2, str(count),
                     va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        busiest_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # ============================================
        # GRAPH 4: Delay Percentage Comparison
        # ============================================
        plt.figure(figsize=(12, 8))

        top_delayed = sorted(
            airport_stats.items(),
            key=lambda x: (x[1]['dep_delay_pct'] + x[1]['arr_delay_pct']) / 2,
            reverse=True
        )[:8]

        airports_delay = [a[0][:15] + '...' if len(a[0]) > 15 else a[0] for a in top_delayed]
        dep_pcts = [a[1]['dep_delay_pct'] for a in top_delayed]
        arr_pcts = [a[1]['arr_delay_pct'] for a in top_delayed]

        x = np.arange(len(airports_delay))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 8))

        bars1 = ax.bar(x - width / 2, dep_pcts, width, label='Departure Delay %',
                       color='blue', alpha=0.7, edgecolor='black')
        bars2 = ax.bar(x + width / 2, arr_pcts, width, label='Arrival Delay %',
                       color='red', alpha=0.7, edgecolor='black')

        ax.set_xlabel('Airport', fontsize=12, fontweight='bold')
        ax.set_ylabel('Delay Percentage', fontsize=12, fontweight='bold')
        ax.set_title('Top 8 Airports by Delay Percentage', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(airports_delay, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                    f'{height:.0f}%', ha='center', va='bottom', fontsize=9)
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 1,
                    f'{height:.0f}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        delay_pct_graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        # Prepare airport list for table
        airport_list = []
        for airport, stats in sorted_airports:
            airport_list.append({
                'name': airport,
                'total_flights': stats['total_flights'],
                'departures': stats['total_departures'],
                'arrivals': stats['total_arrivals'],
                'dep_delay_pct': round(stats['dep_delay_pct'], 1),
                'arr_delay_pct': round(stats['arr_delay_pct'], 1),
                'avg_dep_delay': round(stats['avg_dep_delay'], 1),
                'avg_arr_delay': round(stats['avg_arr_delay'], 1),
                'severe_dep_pct': round(stats['severe_dep_pct'], 1),
                'severe_arr_pct': round(stats['severe_arr_pct'], 1),
                'performance_score': round(stats['performance_score'], 1),
                'performance_rating': stats['performance_rating'],
                'perf_color': stats['perf_color'],
                'congestion_level': stats['congestion_level'],
                'congestion_color': stats['congestion_color'],
                'airlines': stats['airline_count'],
                'busiest_day': stats['busiest_day'],
                'peak_hours': ', '.join([f"{h[0]}" for h in stats['peak_hours']]),
            })

        # Overall statistics
        total_airports = len(airport_stats)
        total_flights_all = sum(s['total_flights'] for s in airport_stats.values())
        total_departures = sum(s['total_departures'] for s in airport_stats.values())
        total_arrivals = sum(s['total_arrivals'] for s in airport_stats.values())
        avg_performance = np.mean([s['performance_score'] for s in airport_stats.values()])

        # Find peak overall hour
        all_hours = defaultdict(int)
        for stats in airport_stats.values():
            for hour, count in stats['hourly_traffic'].items():
                all_hours[hour] += count
        global_peak_hour = max(all_hours, key=all_hours.get) if all_hours else 17

        context = {
            'hourly_graph': hourly_graph,
            'daily_graph': daily_graph,
            'busiest_graph': busiest_graph,
            'delay_pct_graph': delay_pct_graph,
            'airport_list': airport_list,
            'total_airports': total_airports,
            'total_flights': total_flights_all,
            'total_departures': total_departures,
            'total_arrivals': total_arrivals,
            'avg_performance': round(avg_performance, 1),
            'global_peak_hour': f"{global_peak_hour:02d}:00",
            'global_peak_count': all_hours[global_peak_hour],
            'excellent_count': len([a for a in airport_list if a['performance_rating'] == 'Excellent']),
            'good_count': len([a for a in airport_list if a['performance_rating'] == 'Good']),
            'fair_count': len([a for a in airport_list if a['performance_rating'] == 'Fair']),
            'poor_count': len([a for a in airport_list if a['performance_rating'] == 'Poor']),
        }

        return render(request, 'authority/congestionperform.html', context)

    except Exception as e:
        messages.error(request, f"Error analyzing airport congestion: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return redirect('/myapp/authorityhome/')





def flutt_login(request):
    username = request.POST['username']
    password = request.POST['password']
    check = authenticate(request, username=username, password=password)
    print(check)
    if check is not None:
        login(request, check)
        if check.groups.filter(name='passenger').exists():
            return JsonResponse({'status': 'ok', 'lid': check.id})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})


def change_password(request):
    lid = request.POST['lid']
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']

    try:
        user = User.objects.get(id=lid)

        if not user.check_password(old_password):
            return JsonResponse({'status': 'error', 'message': 'Old password incorrect'})

        user.set_password(new_password)
        user.save()

        return JsonResponse({'status': 'ok'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})


def Passenger_view_profile(request):
    lid = request.POST['lid']  # login user id

    passenger = Passenger.objects.get(AUTHUSER__id=lid)

    data = {
        'name': passenger.Name,
        'gender': passenger.Gender,
        'email': passenger.Email,
        'DOB': passenger.DOB,
        'place': passenger.Place,
        'pincode': passenger.Pincode,
        'post': passenger.Post,
        'city': passenger.city,
        'district': passenger.District,  # Capital D
        'state': passenger.State,  # Capital S
        'phoneno': passenger.Phone,  # Phone field (not phoneno)
        'photo': passenger.Photo,  # Capital P
    }

    return JsonResponse({'status': 'ok', 'data': data})


@csrf_exempt
def flutt_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            request.session['user_id'] = user.id

            # Check user type
            try:
                passenger = Passenger.objects.get(AUTHUSER=user)
                return JsonResponse({'status': 'ok', 'lid': passenger.id, 'type': 'passenger'})
            except Passenger.DoesNotExist:
                pass

            try:
                operator = Airline_Operator.objects.get(AUTHUSER=user)
                return JsonResponse({'status': 'ok', 'lid': operator.id, 'type': 'operator'})
            except Airline_Operator.DoesNotExist:
                pass

            try:
                authority = Airport_Authority.objects.get(AUTHUSER=user)
                return JsonResponse({'status': 'ok', 'lid': authority.id, 'type': 'authority'})
            except Airport_Authority.DoesNotExist:
                pass

            return JsonResponse({'status': 'no'})
        else:
            return JsonResponse({'status': 'no'})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def passenger_signup(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            dob = request.POST.get('dob')
            phone = request.POST.get('phoneno')
            gender = request.POST.get('gender')
            place = request.POST.get('place')
            post = request.POST.get('post')
            city = request.POST.get('city')
            district = request.POST.get('district')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')

            # Create User
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()

            # Handle photo upload
            photo = request.FILES.get('photo')
            photo_path = ''
            if photo:
                # Save photo to media folder
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage()
                filename = fs.save(f'passenger_photos/{photo.name}', photo)
                photo_path = fs.url(filename)

            # Create Passenger
            passenger = Passenger.objects.create(
                Name=name,
                Email=email,
                DOB=dob,
                Phone=phone,
                Gender=gender,
                Photo=photo_path,
                Place=place,
                Post=post,
                city=city,
                District=district,
                State=state,
                Pincode=pincode,
                AUTHUSER=user
            )
            passenger.save()

            return JsonResponse({'status': 'ok', 'message': 'Registration successful'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def passenger_view_profile(request):
    if request.method == 'POST':
        lid = request.POST.get('lid')
        try:
            passenger = Passenger.objects.get(id=lid)
            data = {
                'id': passenger.id,
                'name': passenger.Name,
                'email': passenger.Email,
                'dob': str(passenger.DOB),
                'phone': passenger.Phone,
                'gender': passenger.Gender,
                'photo': passenger.Photo,
                'place': passenger.Place,
                'post': passenger.Post,
                'city': passenger.city,
                'district': passenger.District,
                'state': passenger.State,
                'pincode': passenger.Pincode,
            }
            return JsonResponse({'status': 'ok', 'data': data})
        except Passenger.DoesNotExist:
            return JsonResponse({'status': 'no', 'message': 'Passenger not found'})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def passenger_update_profile(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phoneno = request.POST.get('phoneno')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            place = request.POST.get('place')
            pincode = request.POST.get('pincode')
            post = request.POST.get('post')
            city = request.POST.get('city')
            district = request.POST.get('district')
            state = request.POST.get('state')

            passenger = Passenger.objects.get(id=lid)

            # Update fields
            passenger.Name = name
            passenger.Email = email
            passenger.Phone = phoneno
            passenger.DOB = dob
            passenger.Gender = gender
            passenger.Place = place
            passenger.Pincode = pincode
            passenger.Post = post
            passenger.city = city
            passenger.District = district
            passenger.State = state

            # Handle photo upload
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                # Save photo logic here
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage()
                filename = fs.save(f'passenger_photos/{photo.name}', photo)
                photo_path = fs.url(filename)
                passenger.Photo = photo_path

            passenger.save()

            return JsonResponse({'status': 'ok', 'message': 'Profile updated successfully'})
        except Passenger.DoesNotExist:
            return JsonResponse({'status': 'no', 'message': 'Passenger not found'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def view_all_flights(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')  # Passenger ID
            # Get all flights ordered by date and time
            flights = Flight.objects.all().order_by('-Date', '-Time')
            flight_list = []

            for flight in flights:
                # Check if this flight is in passenger's favorites
                is_favorite = False
                if lid and lid.isdigit():
                    try:
                        passenger = Passenger.objects.get(id=lid)
                        favorite = Favorite.objects.get(passenger=passenger, flight=flight)
                        is_favorite = True
                    except (Passenger.DoesNotExist, Favorite.DoesNotExist):
                        pass

                # Get flight schedule if exists
                schedule = Flight_Schedule.objects.filter(FLIGHT=flight).first()

                # Get landing/departure times if exists
                landing_time = None
                if schedule:
                    landing = Flight_LandingdepTime.objects.filter(FLIGHTSCHEDULE=schedule).first()
                    if landing:
                        landing_time = {
                            'arrival': landing.arrivaltime,
                            'departure': landing.departtime
                        }

                flight_data = {
                    'id': flight.id,
                    'flight_name': flight.Flight_Name,
                    'source': flight.Source,
                    'destination': flight.Destination,
                    'date': flight.Date.strftime('%Y-%m-%d'),
                    'time': flight.Time.strftime('%H:%M'),
                    'source_code': flight.Source[:3].upper(),
                    'destination_code': flight.Destination[:3].upper(),
                    'is_favorite': is_favorite,

                    # Schedule data if available
                    'scheduled_departure': schedule.Scheduled_Departure if schedule else None,
                    'scheduled_arrival': schedule.Scheduled_Arrival if schedule else None,
                    'flight_date': schedule.Flight_Date.strftime('%Y-%m-%d') if schedule else None,

                    # Landing/Departure times if available
                    'arrival_time': landing_time['arrival'] if landing_time else None,
                    'departure_time': landing_time['departure'] if landing_time else None,
                }
                flight_list.append(flight_data)

            return JsonResponse({'status': 'ok', 'data': flight_list})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})

@csrf_exempt
def toggle_favorite(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')  # Passenger ID
            flight_id = request.POST.get('flight_id')
            action = request.POST.get('action')  # 'add' or 'remove'

            # You need a Favorite model for this
            passenger = Passenger.objects.get(id=lid)
            flight = Flight.objects.get(id=flight_id)

            if action == 'add':
                favorite = Favorite.objects.create(passenger=passenger, flight=flight)
                favorite.save()
            elif action == 'remove':
                favorite = Favorite.objects.get(passenger=passenger, flight=flight)
                favorite.delete()

            return JsonResponse({'status': 'ok', 'message': 'Favorite updated'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def add_to_favourite(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            flight_id = request.POST.get('flight_id')

            # Similar to toggle_favorite with add action
            passenger = Passenger.objects.get(id=lid)
            flight = Flight.objects.get(id=flight_id)
            favorite = Favorite.objects.create(passenger=passenger, flight=flight)
            favorite.save()

            return JsonResponse({'status': 'ok', 'message': 'Added to favorites'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def remove_favourite(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            flight_id = request.POST.get('flight_id')

            passenger = Passenger.objects.get(id=lid)
            flight = Flight.objects.get(id=flight_id)
            favorite = Favorite.objects.get(passenger=passenger, flight=flight)
            favorite.delete()

            return JsonResponse({'status': 'ok', 'message': 'Removed from favorites'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def remove_multiple_favourites(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            flight_ids_json = request.POST.get('flight_ids')
            flight_ids = json.loads(flight_ids_json)

            passenger = Passenger.objects.get(id=lid)
            for flight_id in flight_ids:
                flight = Flight.objects.get(id=flight_id)
                favorite = Favorite.objects.get(passenger=passenger, flight=flight)
                favorite.delete()

            return JsonResponse({'status': 'ok', 'message': f'{len(flight_ids)} flights removed'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def view_favourite_flights(request):
        lid = request.POST.get('lid')
        passenger = Passenger.objects.get(id=lid)
        favorites = Favorite.objects.filter(passenger=passenger).select_related('flight')
        flight_list = []
        #
        for fav in favorites:
            flight = fav.flight
            flight_data = {
                'id': flight.id,
                'flight_name': flight.Flight_Name,
                'source': flight.Source,
                'destination': flight.Destination,
                'date': str(flight.Date),
                'time': str(flight.Time),
                'added_date': str(fav.created_at.date()) if hasattr(fav, 'created_at') else str(flight.Date),
                'status': 'On Time',
                'available_seats': '150',
                'price': '5000',
                'duration': '2h 30m',
            }
            flight_list.append(flight_data)
        #
        # For now, return empty list
        return JsonResponse({'status': 'ok', 'data': flight_list})


from django.db.models import Count, Q
from datetime import datetime
import random


@csrf_exempt
def get_flight_suggestions(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            source = request.POST.get('source')
            destination = request.POST.get('destination')
            budget = request.POST.get('budget')
            preference = request.POST.get('preference')
            time_preference = request.POST.get('time_preference')
            non_stop_only = request.POST.get('non_stop_only') == 'true'

            # Get all flights matching source and destination (case insensitive)
            flights = Flight.objects.filter(
                Source__icontains=source.strip(),
                Destination__icontains=destination.strip()
            ).order_by('Date', 'Time')

            if not flights.exists():
                return JsonResponse({
                    'status': 'ok',
                    'data': [],
                    'message': f'No flights found from {source} to {destination}'
                })

            # Get user's favorite flights if logged in
            user_favorites = []
            if lid and lid.isdigit():
                try:
                    passenger = Passenger.objects.get(id=lid)
                    user_favorites = Favorite.objects.filter(
                        passenger=passenger
                    ).values_list('flight_id', flat=True)
                except Passenger.DoesNotExist:
                    pass

            flight_list = []
            for flight in flights:
                # Calculate base match score
                match_score = 0.5
                reasons = []

                # 1. Time preference matching
                flight_hour = flight.Time.hour

                if time_preference and time_preference != 'Any':
                    if time_preference == 'Morning (6AM - 12PM)' and 6 <= flight_hour < 12:
                        match_score += 0.2
                        reasons.append("Morning departure")
                    elif time_preference == 'Afternoon (12PM - 6PM)' and 12 <= flight_hour < 18:
                        match_score += 0.2
                        reasons.append("Afternoon departure")
                    elif time_preference == 'Evening (6PM - 9PM)' and 18 <= flight_hour < 21:
                        match_score += 0.2
                        reasons.append("Evening departure")
                    elif time_preference == 'Night (9PM - 6AM)' and (flight_hour >= 21 or flight_hour < 6):
                        match_score += 0.2
                        reasons.append("Night departure")

                # 2. Preference matching
                if preference and preference != 'Any':
                    airline = flight.Flight_Name.split()[0] if flight.Flight_Name else ""

                    if preference == 'Budget Friendly':
                        # Budget friendly flights are usually early morning or late night
                        if flight_hour < 6 or flight_hour > 21:
                            match_score += 0.15
                            reasons.append("Budget friendly timing")

                    elif preference == 'Fastest':
                        # Assume direct flights are faster (you'd need actual duration data)
                        match_score += 0.1
                        reasons.append("Direct flight")

                    elif preference == 'Early Morning':
                        if 4 <= flight_hour < 8:
                            match_score += 0.25
                            reasons.append("Early morning departure")

                    elif preference == 'Late Night':
                        if flight_hour >= 22 or flight_hour < 4:
                            match_score += 0.25
                            reasons.append("Late night departure")

                # 3. Popularity score (based on how many times favorited)
                favorite_count = Favorite.objects.filter(flight=flight).count()
                if favorite_count > 0:
                    popularity_score = min(0.15, favorite_count * 0.03)
                    match_score += popularity_score
                    if favorite_count > 5:
                        reasons.append(f"Popular choice")

                # 4. If user has favorited this flight before
                if flight.id in user_favorites:
                    match_score += 0.2
                    reasons.append("Previously favorited")

                # 5. Weekend/Weekday consideration
                if flight.Date:
                    is_weekend = flight.Date.weekday() >= 5
                    if is_weekend:
                        reasons.append("Weekend flight")

                # Ensure match_score is between 0 and 1
                match_score = min(1.0, max(0.0, match_score))

                # Generate simple insights
                insights = []
                if match_score > 0.8:
                    insights.append("Excellent match for your preferences")
                elif match_score > 0.6:
                    insights.append("Good match based on your criteria")
                elif match_score > 0.4:
                    insights.append("Average match - consider as alternative")
                else:
                    insights.append("Lower match - check other options")

                if reasons:
                    insights.append(f"✓ {reasons[0]}")
                if favorite_count > 0:
                    insights.append(f"❤️ Favorited by {favorite_count} passengers")

                flight_data = {
                    'id': flight.id,
                    'flight_name': flight.Flight_Name,
                    'airline': flight.Flight_Name.split()[0] if flight.Flight_Name else "Unknown",
                    'source': flight.Source,
                    'destination': flight.Destination,
                    'source_code': flight.Source[:3].upper(),
                    'destination_code': flight.Destination[:3].upper(),
                    'date': flight.Date.strftime('%Y-%m-%d'),
                    'time': flight.Time.strftime('%H:%M:%S'),
                    'departure_time': flight.Time.strftime('%H:%M'),
                    'match_score': round(match_score, 2),
                    'match_percentage': int(match_score * 100),
                    'ai_insights': " • ".join(insights[:2]),
                    'reasons': reasons[:2],
                    'is_favorite': flight.id in user_favorites,
                    'favorite_count': favorite_count,
                }
                flight_list.append(flight_data)

            # Sort by match score (highest first)
            flight_list.sort(key=lambda x: x['match_score'], reverse=True)

            # Add summary
            summary = {
                'total_flights': len(flight_list),
                'best_match': flight_list[0]['flight_name'] if flight_list else None,
                'best_match_score': flight_list[0]['match_percentage'] if flight_list else 0,
                'message': f"Found {len(flight_list)} flights from {source} to {destination}"
            }

            if preference and preference != 'Any':
                summary['message'] += f" matching {preference.lower()} preference"

            return JsonResponse({
                'status': 'ok',
                'data': flight_list[:15],  # Limit to top 15
                'summary': summary
            })

        except Exception as e:
            return JsonResponse({
                'status': 'no',
                'message': str(e)
            })

    return JsonResponse({'status': 'no'})


@csrf_exempt
def passenger_send_complaint(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            complaint_text = request.POST.get('complaint')
            date = datetime.now().date()

            passenger = Passenger.objects.get(id=lid)

            complaint = Complaint.objects.create(
                Date=date,
                Complaint=complaint_text,
                Reply='',
                Status='Pending',
                PASSENGER=passenger
            )
            complaint.save()

            return JsonResponse({'status': 'ok', 'message': 'Complaint sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})


@csrf_exempt
def passenger_view_complaints(request):
        lid = request.POST.get('lid')

        passenger = Passenger.objects.get(id=lid)
        complaints = Complaint.objects.filter(PASSENGER=passenger).order_by('-Date')

        complaint_list = []
        for complaint in complaints:
            data = {
                'id': complaint.id,
                'date': str(complaint.Date),
                'complaint': complaint.Complaint,
                'reply': complaint.Reply,
                'status': complaint.Status,
            }
            complaint_list.append(data)

        return JsonResponse({'status': 'ok', 'data': complaint_list})


@csrf_exempt
def passenger_view_reply(request):
        lid = request.POST.get('lid')
        passenger = Passenger.objects.get(id=lid)
        complaints = Complaint.objects.filter(PASSENGER=passenger)

        reply_list = []
        for complaint in complaints:
            data = {
                'id': complaint.id,
                'date': str(complaint.Date),
                'message': complaint.Complaint,
                'reply': complaint.Reply,
                'status': complaint.Status,
                'staff_name': 'Support Team',  # Add staff name logic
            }
            reply_list.append(data)

        return JsonResponse({'status': 'ok', 'data': reply_list})



@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')
            old_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')

            passenger = Passenger.objects.get(id=lid)
            user = passenger.AUTHUSER

            # Check old password
            if not user.check_password(old_password):
                return JsonResponse({'status': 'no', 'message': 'Old password is incorrect'})

            # Set new password
            user.set_password(new_password)
            user.save()

            return JsonResponse({'status': 'ok', 'message': 'Password changed successfully'})
        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})
    return JsonResponse({'status': 'no'})
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Flight
import random

# Global variables for model and encoders
model = None
le_airline = LabelEncoder()
le_source = LabelEncoder()
le_dest = LabelEncoder()


def extract_airline(flight_name):
    """Extract airline name from flight name"""
    if not flight_name:
        return "Unknown"
    # Common airline names
    airlines = ['IndiGo', 'Air India', 'SpiceJet', 'GoAir', 'Vistara', 'AirAsia',
                'Akasa', 'Alliance', 'Star Air', 'TruJet']

    flight_name_upper = flight_name.upper()
    for airline in airlines:
        if airline.upper() in flight_name_upper:
            return airline

    return flight_name.split()[0] if flight_name else "Unknown"


def train_model():
    """Train delay prediction model"""
    global model, le_airline, le_source, le_dest

    # Get flights from database
    flights = Flight.objects.all()

    training_data = []

    if flights.count() > 0:
        # Use actual flight data for patterns
        for flight in flights:
            airline = extract_airline(flight.Flight_Name)

            # Generate synthetic delay based on time patterns
            hour = flight.Time.hour
            base_delay = 0

            # Time-based patterns
            if 6 <= hour <= 10:  # Morning flights
                base_delay = random.randint(0, 15)
            elif 17 <= hour <= 21:  # Evening flights
                base_delay = random.randint(10, 45)
            else:
                base_delay = random.randint(5, 25)

            # Route-based patterns
            busy_routes = [
                ('Mumbai', 'Delhi'), ('Delhi', 'Mumbai'),
                ('Bangalore', 'Chennai'), ('Chennai', 'Bangalore'),
                ('Mumbai', 'Bangalore'), ('Delhi', 'Bangalore')
            ]

            if (flight.Source, flight.Destination) in busy_routes:
                base_delay += random.randint(5, 20)

            # Day of week pattern
            if flight.Date and flight.Date.weekday() >= 5:  # Weekend
                base_delay += random.randint(0, 15)

            training_data.append({
                'airline': airline,
                'source': flight.Source,
                'destination': flight.Destination,
                'hour': hour,
                'minute': flight.Time.minute,
                'delay': base_delay
            })

    # Add synthetic data to ensure enough training samples
    airlines = ['IndiGo', 'Air India', 'SpiceJet', 'GoAir', 'Vistara', 'AirAsia']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad', 'Goa']

    for i in range(100):
        airline = random.choice(airlines)
        source = random.choice(cities)
        dest = random.choice([c for c in cities if c != source])
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)

        # Calculate delay based on factors
        delay = random.randint(0, 30)
        if 17 <= hour <= 21:
            delay += random.randint(10, 30)
        if (source, dest) in [('Mumbai', 'Delhi'), ('Delhi', 'Mumbai'), ('Bangalore', 'Chennai')]:
            delay += random.randint(5, 20)

        training_data.append({
            'airline': airline,
            'source': source,
            'destination': dest,
            'hour': hour,
            'minute': minute,
            'delay': delay
        })

    # Create DataFrame and train model
    df = pd.DataFrame(training_data)

    # Encode categorical variables
    df['airline_encoded'] = le_airline.fit_transform(df['airline'])
    df['source_encoded'] = le_source.fit_transform(df['source'])
    df['dest_encoded'] = le_dest.fit_transform(df['destination'])

    # Features for training
    features = ['airline_encoded', 'source_encoded', 'dest_encoded', 'hour', 'minute']
    X = df[features]
    y = df['delay']

    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)

    # Save model
    joblib.dump(model, 'delay_model.pkl')
    joblib.dump(le_airline, 'airline_enc.pkl')
    joblib.dump(le_source, 'source_enc.pkl')
    joblib.dump(le_dest, 'dest_enc.pkl')


def load_model():
    """Load trained model"""
    global model, le_airline, le_source, le_dest
    try:
        if os.path.exists('delay_model.pkl'):
            model = joblib.load('delay_model.pkl')
            le_airline = joblib.load('airline_enc.pkl')
            le_source = joblib.load('source_enc.pkl')
            le_dest = joblib.load('dest_enc.pkl')
        else:
            train_model()
    except:
        train_model()


# Load model on startup
load_model()


@csrf_exempt
def predict_delay(request):
    """Endpoint to predict flight delay and save prediction"""
    if request.method == 'POST':
        try:
            # Get flight details
            flight_name = request.POST.get('flight_name', '')
            source = request.POST.get('source', '')
            destination = request.POST.get('destination', '')
            date_str = request.POST.get('date', '')
            time_str = request.POST.get('time', '')
            lid = request.POST.get('lid', '')  # Passenger ID

            # Parse date
            flight_date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Check if flight exists in database
            try:
                flight = Flight.objects.get(
                    Flight_Name__icontains=flight_name,
                    Source__icontains=source,
                    Destination__icontains=destination
                )
                flight_exists = True
            except Flight.DoesNotExist:
                flight_exists = False
                flight = None

            # If flight doesn't exist, return error
            if not flight_exists:
                return JsonResponse({
                    'status': 'no',
                    'message': 'Flight not found in database',
                    'error_type': 'flight_not_found'
                })

            # Parse time
            flight_time = datetime.strptime(time_str, '%H:%M:%S').time()

            # Extract features
            hour = flight_time.hour
            minute = flight_time.minute
            airline = extract_airline(flight_name)

            # Encode variables
            try:
                airline_enc = le_airline.transform([airline])[0]
            except:
                airline_enc = 0

            try:
                source_enc = le_source.transform([source])[0]
            except:
                source_enc = 0

            try:
                dest_enc = le_dest.transform([destination])[0]
            except:
                dest_enc = 0

            # Predict delay
            features = [[airline_enc, source_enc, dest_enc, hour, minute]]
            predicted_delay = int(round(model.predict(features)[0]))

            # Determine category
            if predicted_delay <= 15:
                category = "On Time"
                color = "green"
                message = "Your flight is expected to depart on schedule."
            elif predicted_delay <= 30:
                category = "Slight Delay"
                color = "orange"
                message = f"Expected delay of {predicted_delay} minutes."
            elif predicted_delay <= 60:
                category = "Moderate Delay"
                color = "deep_orange"
                message = f"Expected delay of {predicted_delay} minutes. Please check updates."
            else:
                category = "Severe Delay"
                color = "red"
                message = f"Significant delay of {predicted_delay} minutes expected."

            # Calculate estimated departure
            total_minutes = hour * 60 + minute + predicted_delay
            est_hour = (total_minutes // 60) % 24
            est_minute = total_minutes % 60
            estimated_time = f"{est_hour:02d}:{est_minute:02d}:00"
            estimated_time_obj = datetime.strptime(estimated_time, '%H:%M:%S').time()

            # Calculate confidence score (you can make this more sophisticated)
            confidence = 0.85  # Base confidence
            # Adjust based on data availability
            if flight.favorited_by.count() > 10:
                confidence += 0.05
            if Flight.objects.filter(Source=source, Destination=destination).count() > 20:
                confidence += 0.05
            confidence = min(0.98, confidence)

            # Get passenger if logged in
            passenger = None
            if lid and lid.isdigit():
                try:
                    passenger = Passenger.objects.get(id=lid)
                except Passenger.DoesNotExist:
                    pass

            # Save prediction to database
            prediction = FlightDelayPrediction.objects.create(
                passenger=passenger,
                flight=flight,
                flight_name=flight_name,
                source=source,
                destination=destination,
                flight_date=flight_date_obj,
                flight_time=flight_time,
                predicted_delay_minutes=predicted_delay,
                delay_category=category,
                estimated_departure_time=estimated_time_obj,
                confidence_score=round(confidence, 2),
            )

            return JsonResponse({
                'status': 'ok',
                'prediction': {
                    'id': prediction.id,
                    'delay_minutes': predicted_delay,
                    'category': category,
                    'color': color,
                    'message': message,
                    'estimated_departure': estimated_time,
                    'flight_name': flight_name,
                    'source': source,
                    'destination': destination,
                    'confidence': round(confidence, 2),
                    'created_at': prediction.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })

        except Exception as e:
            return JsonResponse({'status': 'no', 'message': str(e)})

    return JsonResponse({'status': 'no'})


import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FlightDelayPrediction, Passenger


@csrf_exempt
def get_prediction_history(request):
    """Get prediction history for a passenger"""
    if request.method == 'POST':
        try:
            lid = request.POST.get('lid')

            if not lid or not lid.isdigit():
                return JsonResponse({
                    'status': 'no',
                    'message': 'Invalid passenger ID'
                })

            # Get passenger
            try:
                passenger = Passenger.objects.get(id=lid)
            except Passenger.DoesNotExist:
                return JsonResponse({
                    'status': 'no',
                    'message': 'Passenger not found'
                })

            # Get predictions for this passenger, ordered by most recent first
            predictions = FlightDelayPrediction.objects.filter(
                passenger=passenger
            ).order_by('-created_at')[:50]  # Limit to last 50

            prediction_list = []
            for pred in predictions:
                # Determine color based on delay category (for Flutter UI)
                color = "green"
                if pred.delay_category == "Slight Delay":
                    color = "orange"
                elif pred.delay_category == "Moderate Delay":
                    color = "deep_orange"
                elif pred.delay_category == "Severe Delay":
                    color = "red"

                prediction_list.append({
                    'id': pred.id,
                    'flight_name': pred.flight_name,
                    'source': pred.source,
                    'destination': pred.destination,
                    'flight_date': pred.flight_date.strftime('%Y-%m-%d'),
                    'flight_time': pred.flight_time.strftime('%H:%M'),
                    'predicted_delay': pred.predicted_delay_minutes,
                    'category': pred.delay_category,
                    'color': color,
                    'estimated_departure': pred.estimated_departure_time.strftime('%H:%M'),
                    'confidence': pred.confidence_score,
                    'created_at': pred.created_at.strftime('%Y-%m-%d %H:%M'),
                    'is_accurate': pred.is_accurate,
                })

            return JsonResponse({
                'status': 'ok',
                'predictions': prediction_list,
                'count': len(prediction_list)
            })

        except Exception as e:
            return JsonResponse({
                'status': 'no',
                'message': str(e)
            })

    return JsonResponse({'status': 'no'})


