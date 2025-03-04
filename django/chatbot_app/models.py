from django.db import models


# Create your models here.
class Message(models.Model):
    user_message = models.TextField()
    bot_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
