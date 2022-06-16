from django.urls import path

from . import views

urlpatterns=[
    path('', views.home, name='movie-review-home'),
    path('info/', views.info, name='movie-review-info'),
]