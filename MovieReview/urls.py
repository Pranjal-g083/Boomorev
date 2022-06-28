from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='movie-review-home'),
    path('trending/', views.trending, name='trending'),
    path('genre/<str:genre_name>/', views.genre, name='movie-genre-home'),
    path('movie/<int:id>/', views.info, name='movie-review-info'),
    path('AboutUs/', views.about, name='about-us'),
    # path('search/<str:search_name>/', views.search, name='movie-search'),
]