from django.db import models

# Create your models here.


from django.db import models

class CampusConnect(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=15)
    institution_name = models.CharField(max_length=255)
    institution_city = models.CharField(max_length=100)
    institution_state = models.CharField(max_length=100)
    institution_country = models.CharField(max_length=100)
    institution_address = models.CharField(max_length=255)
    institution_postal_code = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Campus Lite"
        verbose_name_plural = "Campus Lite"

    def __str__(self):
        return self.full_name
