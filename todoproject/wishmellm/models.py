from django.db import models

# Create your models here.
class Wish(models.Model):
    qr = models.ImageField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        
