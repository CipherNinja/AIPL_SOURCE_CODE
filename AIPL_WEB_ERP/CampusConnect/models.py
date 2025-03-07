from django.db import models

# Create your models here.


from django.db import models

class CampusConnect(models.Model):
    LEAD_STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    remark = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "Campus Lite"
        verbose_name_plural = "Campus Lite"

    def __str__(self):
        return self.full_name
