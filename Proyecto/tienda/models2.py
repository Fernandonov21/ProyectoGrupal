from django.db import models
from django.contrib.auth.models import User

class Queja(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    asunto = models.CharField(max_length=200)
    description_queja = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    resolved_queja = models.BooleanField(default=False)
    positive_queja = models.BooleanField(default= False)
    negative_queja = models.BooleanField(default=False)
    datecompletedqueja = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.asunto + ' - ' + self.user.username
