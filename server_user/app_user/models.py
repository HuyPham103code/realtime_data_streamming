from django.db import models

# Create your models here.

class Employee(models.Model):
    address = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)  # male or female
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    picture = models.URLField()
    post_code = models.CharField(max_length=10)
    registered_date = models.DateTimeField()
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username