from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField(null=True, blank=True)
    year = models.IntegerField()
    imdb_url = models.CharField(max_length=200)
    trailer = models.CharField(max_length=200)
    publish_date = models.DateTimeField(default=timezone.now)
    image=models.ImageField(upload_to='images/',default='default.jpg')
    genres=models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = RichTextField()
    publish_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text
    