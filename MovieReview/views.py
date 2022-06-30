from unittest import result
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import json
from urllib.request import urlopen

import urllib.parse
from .forms import ReplyForm, CommentEditForm, ReplyEditForm
from .models import Comment, Reply, Likes, Upvote, Downvote, UserRating




# load the api key from a local file since the api key shall not be shared in the code itself for secuirty reasons
api_key = json.load(open("api.json", "r"))
API_KEY = api_key["key"]
API_HOST = "https://api.themoviedb.org/3/"

YT_EMBED = "https://www.youtube.com/embed/"


url = API_HOST + "genre/movie/list?api_key=" + API_KEY
response = urlopen(url)
genre_list = json.load(response)



# generates the html for the home page


def home(request):
    context = []
    url = API_HOST + "movie/popular?api_key=" + API_KEY
    # can add &language=en-US&page=1 to the url to get the english version of the movie
    response = urlopen(url)
    movies = json.load(response)
    valid_movies = []

    for movie in movies["results"]:
        if movie["backdrop_path"]:
            valid_movies.append(movie)
        

    if request.method == 'POST':
        if "search_result_form" in request.POST:
            url= API_HOST+"search/movie?api_key="+ API_KEY +'&query=' + urllib.parse.quote_plus(request.POST.get('search_name')) 
            response = urlopen(url)
            movies = json.load(response)
            valid_movies = []

            for movie in movies["results"]:
                if movie["backdrop_path"]:
                    valid_movies.append(movie)
                param = {"movies": valid_movies, "genres": genre_list,
                    "current_genre": {'name':request.POST.get('search_name')}, "title": request.POST.get('search_name')}
        
            return render(request, 'MovieReview/home.html', param)
    param = {"movies": valid_movies, "genres": genre_list}
    return render(request, 'MovieReview/home.html', param)

def about(request):
    return render(request, 'MovieReview/aboutUs.html');

def genre(request, genre_name):
    context = []
    cur_gen = {"name": genre_name}
    for genre in genre_list["genres"]:
        if genre["name"] == genre_name:
            cur_gen["id"] = genre["id"]

    url = API_HOST + "discover/movie?api_key=" + API_KEY + \
        "&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=" + \
        str(cur_gen["id"])+"&with_watch_monetization_types=flatrate"
    response = urlopen(url)
    movies = json.load(response)
    valid_movies = []

    for movie in movies["results"]:
        if movie["backdrop_path"]:
            valid_movies.append(movie)
    if request.method == 'POST':
        if "search_result_form" in request.POST:
            url= API_HOST+"search/movie?api_key="+ API_KEY +'&query=' + urllib.parse.quote_plus(request.POST.get('search_name')) 
            response = urlopen(url)
            movies = json.load(response)
            valid_movies = []

            for movie in movies["results"]:
                if movie["backdrop_path"]:
                    valid_movies.append(movie)
            param = {"movies": valid_movies, "genres": genre_list,
                    "current_genre": {'name':request.POST.get('search_name')}, "title": request.POST.get('search_name')}
        
            return render(request, 'MovieReview/home.html', param)
    param = {"movies": valid_movies, "genres": genre_list,
             "current_genre": cur_gen, "title": genre_name}
    return render(request, 'MovieReview/home.html', param)


def info(request, id):

    # get the details of the movie along with trailer and videos
    url = API_HOST + "movie/" + str(id) + "?api_key=" + API_KEY + \
        "&language=en-US&append_to_response=videos"
    response = urlopen(url)
    movie = json.load(response)

    # get recommendation based on the movie
    url = API_HOST+"movie/" + \
        str(id) + "/recommendations?api_key=" + API_KEY + "&language=en-US"
    response = urlopen(url)
    recommendations = json.load(response)

    # set trailer to official trailer if available, otherwise official trailer, else any other available video.
    # if none found, add a broken link
    trailer = []
    for vid in movie["videos"]["results"]:
        if vid["type"] == "Trailer":
            if vid["site"] == "YouTube":
                if vid["official"]:
                    trailer.append(YT_EMBED + vid["key"])
    for vid in movie["videos"]["results"]:
        if vid["type"] == "Teaser":
            if vid["site"] == "YouTube":
                if vid["official"]:
                    trailer.append(YT_EMBED + vid["key"])
    for vid in movie["videos"]["results"]:
        trailer.append(YT_EMBED + vid["key"])
    trailer.append(YT_EMBED + "no_video_found")
    title = movie["title"]
    
    comments = Comment.objects.filter(movieid=str(id)).order_by('-added_on')
    if request.user.is_authenticated:
        for comment in comments:
            
            chk = Likes.objects.filter(comment=comment, user=request.user)
            if chk.exists():
                comment.like=True

        

    if request.method == 'POST':

        if 'comment_add_form' in request.POST:
            if(request.user.is_authenticated):
                obj = Comment.objects.create(
                    movieid=id, commented_by=request.user, comment=request.POST['comment'])
                obj.save()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'reply_add_form' in request.POST:
            reply_add_form = ReplyForm(request.POST)
            if(request.user.is_authenticated):
                if(reply_add_form.is_valid()):
                    obj = reply_add_form.save(commit=False)
                    obj.comment = Comment.objects.filter(
                        pk=request.POST.get('parent_id')).first()
                    obj.user = request.user
                    obj.save()
                    return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'comment_delete_form' in request.POST:
            obj = Comment.objects.filter(pk=request.POST.get('object_id'))
            obj.delete()
            return HttpResponseRedirect(reverse('movie-review-info', args=[id]))

        if 'reply_delete_form' in request.POST:
            obj = Reply.objects.filter(pk=request.POST.get('object_id'))
            obj.delete()
            return HttpResponseRedirect(reverse('movie-review-info', args=[id]))

        if 'comment_upvote_form' in request.POST:
            if(request.user.is_authenticated):
                comment = Comment.objects.get(pk=request.POST.get('object_id'))
                chkup = Upvote.objects.filter(comment=comment, user=request.user)
                chkdown = Downvote.objects.filter(comment=comment, user=request.user)
                if chkup.exists() == False : 
                    obj = Upvote(comment=comment, user=request.user)
                    obj.save()
                    if chkdown.exists():
                        chkdown = chkdown.first()
                        chkdown.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'comment_downvote_form' in request.POST:
            if(request.user.is_authenticated):
                comment = Comment.objects.get(pk=request.POST.get('object_id'))
                chkdown = Downvote.objects.filter(comment=comment, user=request.user)
                chkup = Upvote.objects.filter(comment=comment, user=request.user)
                if chkdown.exists() == False:
                    obj = Downvote(comment=comment, user=request.user)
                    obj.save()
                    if chkup.exists():
                        chkup = chkup.first()
                        chkup.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'comment_like_form' in request.POST:
            if(request.user.is_authenticated):
                comment = Comment.objects.get(pk=request.POST.get('object_id'))
                chklike = Likes.objects.filter(comment=comment, user=request.user)
                if chklike.exists() == False:
                    obj = Likes(comment=comment, user=request.user)
                    obj.save()
                else:
                    chklike = chklike.first()
                    chklike.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'reply_upvote_form' in request.POST:
            if(request.user.is_authenticated):
                reply = Reply.objects.get(pk=request.POST.get('object_id'))
                chkup = Upvote.objects.filter(reply=reply, user=request.user)
                chkdown = Downvote.objects.filter(reply=reply, user=request.user)
                if chkup.exists() == False:
                    obj = Upvote(reply=reply, user=request.user)
                    obj.save()
                    if chkdown.exists() : 
                        chkdown = chkdown.first()
                        chkdown.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'reply_downvote_form' in request.POST:
            if(request.user.is_authenticated):
                reply = Reply.objects.get(pk=request.POST.get('object_id'))
                chkdown = Downvote.objects.filter(reply=reply, user=request.user)
                chkup = Upvote.objects.filter(reply=reply, user=request.user)
                if chkdown.exists() == False:
                    obj = Downvote(reply=reply, user=request.user)
                    obj.save()
                    if chkup.exists():
                        chkup = chkup.first()
                        chkup.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'reply_like_form' in request.POST:
            if(request.user.is_authenticated):
                reply = Reply.objects.get(pk=request.POST.get('object_id'))
                chklike = Likes.objects.filter(reply=reply, user=request.user)
                if chklike.exists() == False:
                    obj = Likes(reply=reply, user=request.user)
                    obj.save()
                else:
                    chklike = chklike.first()
                    chklike.delete()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'comment_edit_form' in request.POST:
            comment_edit_form = CommentEditForm(request.POST)
            if(comment_edit_form.is_valid()):
                obj = Comment.objects.get(pk=request.POST.get('object_id'))
                obj.comment = comment_edit_form.cleaned_data['comment']
                obj.save()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))

        if 'reply_edit_form' in request.POST:
            reply_edit_form = ReplyEditForm(request.POST)
            if(reply_edit_form.is_valid()):
                obj = Reply.objects.get(pk=request.POST.get('object_id'))
                obj.reply = reply_edit_form.cleaned_data['reply']
                obj.save()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))

        if 'rating_form' in request.POST:
            if(request.user.is_authenticated):
                obj = UserRating.objects.filter(
                    user=request.user, movieid=str(id))
                if obj.exists():
                    obj = obj.first()
                    obj.rating = request.POST.get('rating_form')
                else:
                    obj = UserRating(user=request.user, movieid=str(
                        id), rating=request.POST.get('rating_form'))
                obj.save()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if 'movie_like_form' in request.POST:
            if(request.user.is_authenticated):
                obj = UserRating.objects.filter(
                    user=request.user, movieid=str(id))
                if obj.exists():
                    obj = obj.first()
                    if obj.like == True:
                        obj.like = False
                    else:
                        obj.like = True
                else:
                    obj = UserRating(user=request.user,
                                     movieid=str(id), like=True)
                obj.save()
                return HttpResponseRedirect(reverse('movie-review-info', args=[id]))
            else:
                messages.success(request, f'Please login in first')
                return redirect('login')

        if request.method == 'POST':
            if "search_result_form" in request.POST:
                url= API_HOST+"search/movie?api_key="+ API_KEY +'&query=' + urllib.parse.quote_plus(request.POST.get('search_name')) 
                response = urlopen(url)
                movies = json.load(response)
                valid_movies = []

                for movie in movies["results"]:
                    if movie["backdrop_path"]:
                        valid_movies.append(movie)
                param = {"movies": valid_movies, "genres": genre_list,
                        "current_genre": {'name':request.POST.get('search_name')}, "title": request.POST.get('search_name')}
            
                return render(request, 'MovieReview/home.html', param)

    # comment_add_form = CommentForm()
    reply_add_form = ReplyForm()
    comment_edit_form = CommentEditForm()
    reply_edit_form = ReplyEditForm()

    if(request.user.is_authenticated):
        obj = UserRating.objects.filter(user=request.user, movieid=str(id))
        if obj.exists():
            rating = obj.first().rating
            movie_like = obj.first().like
        else:
            rating = 0
            movie_like = False
    else:
        rating = 0
        movie_like = False

    # like_replys = []

    if(request.user.is_authenticated):
        for comment in comments:

            replys = Reply.objects.filter(comment=comment,user=request.user)
            # like_reply = []
            for reply in replys:
                chk = Likes.objects.filter(comment=comment, user=request.user)
                if chk.exists():
                    reply.like=True
                else:
                    reply.like=False
            
            # like_replys.append(like_reply)
    user_ratings = UserRating.objects.filter(movieid=id)
    count = 0;
    sum = 0;
    for user_rating in user_ratings:
        if user_rating.rating != 0:
            count = count+1
            sum = sum + user_rating.rating
    average="No Ratings yet"
    if count:
        average = str(round((sum/count)*2,1))+"/10"
    param = {"comments": comments,
             "movie": movie,
             "recommendations": recommendations,
             "trailer": trailer[0],
             "title": title,
             "reply_add_form": reply_add_form,
             #  "comment_add_form": comment_add_form,
             "comment_edit_form": comment_edit_form,
             "reply_edit_form": reply_edit_form,
             "rating": rating,
             "rating5": 5 - rating,
             "movie_like": movie_like,
             "average": average,
             }

    return render(request, 'MovieReview/info.html', param)


def india(request):
    url = API_HOST + "discover/movie/?api_key=" + API_KEY + "&sort_by=vote_average.desc&vote_count.gte=25&with_original_language=hi"
    response = urlopen(url)
    movies = json.load(response)

    valid_movies = []

    for movie in movies["results"]:
        if movie["backdrop_path"]:
            valid_movies.append(movie)

    for movie in movies["results"]:
        like = UserRating.objects.filter(movieid = movie["id"],like=True).count()
        movie["user_like"] = like

    return render(request, 'MovieReview/trending.html', {"results": valid_movies})
