from django.shortcuts import render, get_object_or_404
from multiprocessing import context
from django.http import HttpResponse
from .models import Movie, Review
# Create your views here.
import json
from urllib.request import urlopen
url="https://api.themoviedb.org/3/movie/popular?api_key=8511985aaf3fd8b644f3956666ae4679&language=en-US&page=1&append_to_response=videos";
response = urlopen(url);
context= json.load(response);
# context = json.load(open('./movie.json','r',encoding="utf8"))
context_2= json.load(open('./genre.json','r',encoding="utf8"))
# print( context);
def home(request):
    return render(request, 'moviereview/home.html',{'result':context, 'genres':context_2})

def info(request,id):
    response_1= urlopen(f'https://api.themoviedb.org/3/movie/{id}?api_key=8511985aaf3fd8b644f3956666ae4679&language=en-US&append_to_response=videos');
    response_2=urlopen(f'https://api.themoviedb.org/3/movie/{id}/recommendations?api_key=8511985aaf3fd8b644f3956666ae4679&language=en-US&page=1')
    context_3= json.load(response_1);
    recommendations= json.load(response_2);
    return render(request, 'moviereview/info.html',{'result':context_3, 'recommendations':recommendations["results"]})

def genre(request,id):
    response_1= urlopen(f'https://api.themoviedb.org/3/discover/movie?api_key=8511985aaf3fd8b644f3956666ae4679&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres={id}&with_watch_monetization_types=flatrate');
    context_3= json.load(response_1);
    return render(request, 'moviereview/home.html',{'result':context_3, 'genres':context_2})