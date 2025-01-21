from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    todoTitle=models.CharField((""), max_length=100)
    todoDescription=models.CharField((""), max_length=500)
