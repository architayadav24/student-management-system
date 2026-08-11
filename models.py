from django.db import models

# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=30,null=True)
    email=models.CharField(max_length=30,null=True)
    username=models.CharField(max_length=30,unique=True,blank=True)
    password=models.CharField(max_length=30,blank=True)
    college=models.CharField(max_length=30,null=True)
    address=models.CharField(max_length=30,null=True)
    join_date=models.CharField(max_length=30,null=True)
    total_fee=models.CharField(max_length=30,null=True)
    paid_fee=models.CharField(max_length=30,null=True)
    due_fee=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    technology=models.CharField(max_length=30,null=True)
    image=models.FileField()

class Feedback(models.Model):
    name=models.CharField(max_length=30,null=True) 
    email=models.CharField(max_length=30,null=True) 
    feedback=models.TextField()

