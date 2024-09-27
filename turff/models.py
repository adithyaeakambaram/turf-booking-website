
from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class GameCatagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    game_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    status = models.BooleanField(default=False, help_text="0-show, 1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TurfCatagory(models.Model):
    game_category = models.ForeignKey(GameCatagory, on_delete=models.CASCADE, related_name='turfs')
    name = models.CharField(max_length=150, null=False, blank=False)
    turf_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show, 1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True, help_text="True-Available, False-Not Available")
    day_choices = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')
    ]
    total_cost = models.FloatField(null=False, blank=False)
    day = models.CharField(max_length=10, choices=day_choices, null=False, blank=False)
    opening_time = models.TimeField(null=False, blank=False)
    closing_time = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.name
    
class Bookingss(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(TurfCatagory, on_delete=models.CASCADE, related_name='bookings')
    game_category = models.ForeignKey(GameCatagory, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(null=False, blank=False)
    time_slot = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    game_name = models.CharField(max_length=150, null=False, blank=False)
    game_description = models.TextField(max_length=500, null=False, blank=False)
    turf_name = models.CharField(max_length=150, null=False, blank=False)
    turf_description = models.TextField(max_length=500, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('turf', 'booking_date', 'time_slot')

    def __str__(self):
        return f"{self.turf.name} - {self.booking_date} - {self.time_slot}"
    
    




