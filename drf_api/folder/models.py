from django.db import models
from user.models import UserProfile

class Folder(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="folders")    

    def __str__(self):
        return self.name