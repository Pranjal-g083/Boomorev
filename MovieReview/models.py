from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image

# Create your models here.
# class Movie(models.Model):
#     title = models.CharField(max_length=200)
#     description = RichTextField(null=True, blank=True)
#     year = models.IntegerField()
#     imdb_url = models.CharField(max_length=200)
#     trailer = models.CharField(max_length=200)
#     publish_date = models.DateTimeField(default=timezone.now)
#     image=models.ImageField(upload_to='images/',default='default.jpg')
#     genres=models.CharField(max_length=200,null=True,blank=True)

#     def __str__(self):
#         return self.title
    

# class Review(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     text = RichTextField()
#     publish_date = models.DateTimeField(default=timezone.now)
    
#     def __str__(self):
#         return self.text


class Comment(models.Model):

    movieid = models.CharField(max_length=100)
    comment = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.comment

    @classmethod
    def get_all(cls):
        return cls.objects.all()


class Reply(models.Model):

    reply = models.TextField()
    comment = models.ForeignKey(Comment, related_name='replies',  on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.reply

    class Meta:
        ordering = ['-added_on']

    @property
    def get_replies(self):
        return self.replies.all()

class Likes(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, null=True,related_name='likes',on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply,null=True,related_name='likes',on_delete=models.CASCADE)

class Upvote(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, null=True,related_name='upvote',on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply,null=True,related_name='upvote',on_delete=models.CASCADE)

class Downvote(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment,related_name='downvote', null=True,on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply,null=True,related_name='downvote',on_delete=models.CASCADE)

class UserRating(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movieid = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    like = models.BooleanField(default=False)
    