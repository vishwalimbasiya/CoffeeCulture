from django.db import models

# Create your models here.

class signupMaster(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    zipcode=models.IntegerField()

    def __str__(self):
        return self.fname

class notes(models.Model):
    title=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    selectfile=models.FileField(upload_to="notes")
    comments=models.TextField()
