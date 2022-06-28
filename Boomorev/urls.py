"""Boomorev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from User import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import LoginView,SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MovieReview.urls')),
    path('register/',SignupView.as_view(template_name='User/register.html'),name='register'),
    path('login/',LoginView.as_view(template_name='User/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='User/logout.html'),name='logout'),
    path('profile/',user_views.profile,name='profile'),
    path('Update/',user_views.update,name='update'),
    path('', include('allauth.urls')),

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
