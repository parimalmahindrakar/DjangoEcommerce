from django.db import models

# Create your models here.
class PostalCodes(models.Model):
    area = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    code = models.PositiveIntegerField()

    def __str__(self):
        return self.area
