from django.urls import path

from . import views

urlpatterns=[
    path('', views.home, name='movie-review-home'),
    path('info/<int:id>', views.info, name='movie-review-info'),
    path('genre/<int:id>', views.genre, name='movie-review-genre'),
]