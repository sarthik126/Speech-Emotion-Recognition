from django.db import models

# Create your models here.
class ValueTable(models.Model):
    value1 = models.CharField(max_length=30, blank=True)

    def __str__(self):
    	return self.value1