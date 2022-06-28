from django.shortcuts import render, redirect
# from django.contrib.auth.forms import RegisterForm
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from urllib.request import urlopen
from MovieReview.models import Comment,Reply,UserRating,Likes
from django.contrib.auth.models import User
from allauth.account.forms import ResetPasswordForm
import urllib

api_key = json.load(open("api.json", "r"))
API_KEY = api_key["key"]
API_HOST = "https://api.themoviedb.org/3/"

genre_list = json.load(open("genre.json", "r"))

def register(request):
    if request.method== 'POST':
        form= RegisterForm(request.POST)
        if(form.is_valid()):
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!Please Login')
            form.save()
            return redirect('login')
    else:
        form= RegisterForm()
    return render(request, 'User/register.html', {'form': form})   
 
@login_required
def profile(request):

    if request.method == 'POST':
        if "search_result_form" in request.POST:
            url= API_HOST+"search/movie?api_key="+ API_KEY +'&query=' + urllib.parse.quote_plus(request.POST.get('search_name')) 
            response = urlopen(url)
            movies = json.load(response)
            param = {"movies": movies["results"], "genres": genre_list,
                    "current_genre": {'name':request.POST.get('search_name')}, "title": request.POST.get('search_name')}
        
            return render(request, 'MovieReview/home.html', param)

    comments = Comment.objects.filter(commented_by = request.user).order_by('-added_on')
    reply = Reply.objects.filter(user = request.user).order_by('-added_on')

    for comment in comments:
        
        url = API_HOST + "movie/" + str(comment.movieid) + "?api_key=" + API_KEY
        response = urlopen(url)
        movie = json.load(response)
        comment.poster = movie["backdrop_path"]
        comment.movie_name = movie["title"]
        
    context = []
    movies = UserRating.objects.filter(user = request.user,like=True)
    for movie in movies:
        url = API_HOST + "movie/" + str(movie.movieid) + "?api_key=" + API_KEY
        response = urlopen(url)
        movie = json.load(response)
        context.append(movie)
        
    params = {'comments':comments , 'replys' : reply , 'movies' : context}
    # return render(request, 'User/profile2.html',params)
    return render(request, 'User/profile.html',params)


@login_required
def update(request):
    if request.method == 'POST':
        u_form= UserUpdateForm(request.POST,instance=request.user);
        p_form= ProfileUpdateForm(request.POST
                                  ,request.FILES
                                  ,instance=request.user.profile);
        if u_form.is_valid() and p_form.is_valid():
            u_form.save();
            p_form.save();
            messages.success(request,f'Account updated successfully!');
            return redirect('profile')
    else:
        u_form= UserUpdateForm(instance=request.user);
        p_form= ProfileUpdateForm(instance=request.user.profile);
    context= {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'User/profile_update.html',context);