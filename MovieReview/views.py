from django.shortcuts import render, get_object_or_404
from multiprocessing import context
from django.http import HttpResponse
from .models import Movie, Review
# Create your views here.
import json
context = json.load(open('./movie.json','r',encoding="utf8"))
context_2= json.load(open('./genre.json','r',encoding="utf8"))
# print( context);
def home(request):
    return render(request, 'moviereview/home.html',context)

def info(request,id):
    for(result) in context['results']:
        if result['id']==id:
            return render(request, 'moviereview/info.html',{'result':result,'genres':context_2['genres']})
    # return render(request, 'moviereview/info.html')
    else:
        return HttpResponse('<h1>Not Found</h1>');