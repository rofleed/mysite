from django.db import models

# Create your models here.
class HistoryInfo6 (models.Model):

    app_key = models.CharField(max_length = 32)
    proctime = models.CharField(max_length= 32)
    datanum = models.CharField(max_length= 32)
    env = models.CharField(max_length= 32)