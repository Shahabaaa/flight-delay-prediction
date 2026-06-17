from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Passenger(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    DOB=models.DateField()
    Phone=models.CharField(max_length=100)
    Gender=models.CharField(max_length=100)
    Photo=models.CharField(max_length=400)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    District=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    Pincode=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)

class Airline_Operator(models.Model):
    Full_Name=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    Phone=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    DOB=models.DateField()
    Photo=models.CharField(max_length=100)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    District=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    Pincode=models.CharField(max_length=100)
    Proof=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)


class Airport_Authority(models.Model):
    Full_Name=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    Phone=models.CharField(max_length=100)
    Gender=models.CharField(max_length=100)
    DOB=models.DateField()
    Photo=models.CharField(max_length=100)
    Place=models.CharField(max_length=100)
    Post=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    District=models.CharField(max_length=100)
    State=models.CharField(max_length=100)
    Pincode=models.CharField(max_length=100)
    Proof=models.CharField(max_length=400)
    AUTHUSER = models.OneToOneField(User, on_delete=models.CASCADE)

class Flight(models.Model):
    Flight_Name=models.CharField(max_length=100)
    Source=models.CharField(max_length=100)
    Destination=models.CharField(max_length=100)
    Date=models.DateField()
    Time=models.TimeField()


class Flight_Schedule(models.Model):
    Flight_Date=models.DateField()
    Scheduled_Departure=models.CharField(max_length=100)
    Scheduled_Arrival=models.CharField(max_length=100)
    FLIGHT=models.ForeignKey(Flight,on_delete=models.CASCADE)

class Flight_LandingdepTime(models.Model):
    Date=models.DateField()
    Time=models.TimeField()
    arrivaltime=models.CharField(max_length=100)
    departtime=models.CharField(max_length=100)
    FLIGHTSCHEDULE=models.ForeignKey(Flight_Schedule,on_delete=models.CASCADE)


class Complaint(models.Model):
    Date=models.DateField()
    Complaint=models.CharField(max_length=200)
    Reply=models.CharField(max_length=200)
    Status=models.CharField(max_length=200)
    PASSENGER=models.ForeignKey(Passenger,on_delete=models.CASCADE)


class Favorite(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='favorites')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('passenger', 'flight')  # Prevent duplicate favorites

    def __str__(self):
        return f"{self.passenger.Name} - {self.flight.Flight_Name}"


class FlightDelayPrediction(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='delay_predictions')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='delay_predictions')

    # Input data
    flight_name = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    flight_date = models.DateField()
    flight_time = models.TimeField()

    # Prediction results
    predicted_delay_minutes = models.IntegerField()
    delay_category = models.CharField(max_length=50)  # On Time, Slight Delay, etc.
    estimated_departure_time = models.TimeField()

    # Metadata
    confidence_score = models.FloatField(default=0.0)  # Optional: confidence of prediction
    created_at = models.DateTimeField(auto_now_add=True)
    is_accurate = models.BooleanField(null=True, blank=True)  # For future feedback

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['passenger', '-created_at']),
            models.Index(fields=['flight', '-created_at']),
        ]

    def __str__(self):
        return f"{self.flight_name} - {self.predicted_delay_minutes} mins delay on {self.created_at.date()}"