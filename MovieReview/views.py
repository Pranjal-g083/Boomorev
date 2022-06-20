from django.shortcuts import render, get_object_or_404
from multiprocessing import context
from django.http import HttpResponse
from .models import Movie, Review
import json
from urllib.request import urlopen

api_key = json.load(open("api.json","r"))
ApiKey = api_key["key"]


def home(request):
    context = []
    url = "https://api.themoviedb.org/3/movie/top_rated?api_key=" + ApiKey + "&language=en-US&page=1"
    response = urlopen(url)
    movies = json.load(response)

    for movie in movies["results"]:
        url1 = "https://api.themoviedb.org/3/movie/" + \
            str(movie["id"]) + \
            "?api_key=" + ApiKey + "&language=en-US&append_to_response=videos"
        response = urlopen(url1)
        data = json.load(response)
        context.append(data)
    param = { "movies": context }
    return render(request, 'MovieReview/home.html', param)


def info(request,id):
    url = "https://api.themoviedb.org/3/movie/" + \
            str(id) + \
            "?api_key=" +ApiKey+"&language=en-US&append_to_response=videos"
    response = urlopen(url)
    movie = json.load(response)

    url = "https://api.themoviedb.org/3/movie/" + \
        str(id) + \
        "/recommendations?api_key=" + ApiKey+ "&language=en-US"
    response = urlopen(url)
    recommendations = json.load(response)
    trailer = []
    for vid in movie["videos"]["results"]:
        if vid["type"] == "Trailer":
            if vid["site"] == "YouTube":
                if vid["official"]:
                    trailer.append("https://www.youtube.com/embed/" + vid["key"])
    trailer.append("https://www.youtube.com/embed/no_video_found")
    param = { "movie": movie, "recommendations": recommendations , "trailer": trailer[0]}
    return render(request, 'MovieReview/info.html',param)
