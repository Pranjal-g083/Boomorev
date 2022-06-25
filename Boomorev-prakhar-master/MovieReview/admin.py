from django.contrib import admin
from .models import Comment,Reply,Likes,Upvote,Downvote,UserRating

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Likes)
admin.site.register(Upvote)
admin.site.register(Downvote)
admin.site.register(UserRating)