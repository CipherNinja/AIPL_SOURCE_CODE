from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

# Create your models here.

class dataDeletionModel(models.Model):
    choice_for_deletion = [
    ('privacy concern','Privacy Concern'),
    ('security concern','Security Concern'),
    ('no longer needed','No Longer Needed'),
    ('regulatory request (e.g. gdpr/ccpa)','Regulatory Request (e.g. GDPR/CCPA)'),
    ('other','Other'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.CharField(choices=choice_for_deletion,max_length=55)
    additional_info = models.TextField(max_length=1500)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        verbose_name = "Data Deletion Request"
        verbose_name_plural = "Data Deletion Requests"


# Same model will be used if we want to set meeting with developer, HR etc
class Meeting(models.Model):
    REASON_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Support', 'Support'),
        ('Demo', 'Demo'),
        ('Product Demonstration', 'Product Demonstration'),
        ('Business Development', 'Business Development'),
        ('Strategic Planning', 'Strategic Planning'),
        ('Project Kickoff', 'Project Kickoff'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetings')
    date = models.DateField()  # Date of the meeting
    time = models.TimeField()  # Time of the meeting
    timezone = models.CharField(max_length=100, default='UTC')  # Time zone of the meeting
    location = models.CharField(max_length=255)  # Location of the meeting
    reason = models.CharField(choices=REASON_CHOICES, max_length=50)  # Reason for the meeting
    description = models.TextField()  # Additional details about the meeting
    created_at = models.DateTimeField(auto_now_add=True)  # When the meeting was scheduled

    def __str__(self):
        return f"Meeting on {self.date} at {self.time} with {self.user.username}"

    class Meta:
        ordering = ['date', 'time']
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"
