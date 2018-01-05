from django.db import models

# Create your models here.
class HistoryInfo8 (models.Model):

    app_key = models.CharField(max_length = 32)
    proctime = models.CharField(max_length= 32)
    datanum = models.CharField(max_length= 32)
    env = models.CharField(max_length= 32)
    nowtime = models.CharField(max_length= 32)
    result = models.CharField(max_length= 32)
