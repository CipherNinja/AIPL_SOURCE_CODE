from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
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