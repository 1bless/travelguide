from django.db import models

class UserPreference(models.Model):
    user_name = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    # Add more fields as needed

    def __str__(self):
        return self.user_name