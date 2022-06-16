from django.shortcuts import render, get_object_or_404
from multiprocessing import context
from django.http import HttpResponse
from .models import Movie, Review
# Create your views here.

def home(request):
    return render(request, 'moviereview/home.html')

def info(request):
    return render(request, 'moviereview/info.html')