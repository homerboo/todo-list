from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)




