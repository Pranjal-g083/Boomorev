from django.shortcuts import render, get_object_or_404
from multiprocessing import context
from django.http import HttpResponse
from .models import Movie, Review
import json
context = json.load(open('./movie.json','r'))
# Create your views here.

def home(request):
    return render(request, 'MovieReview/home.html', context)

def info(request):
    return render(request, 'MovieReview/info.html')
