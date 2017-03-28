"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from memcpy import home_views, user_views, book_views

urlpatterns = [
    # Home page
    url(r'^$', home_views.home, name='home'),
    # Built-in authentication with our own template login page
    url(r'^login[/]?$', auth_views.login, {'template_name': 'memcpy/login.html'}, name='login'),
    # Logout a user and send them back to the login page
    url(r'^logout[/]?$', user_views.logout, name='logout'),
    # User registration
    url(r'^register$', user_views.register, name='register'),
    # Browse all books
    url(r'^books[/]?$', book_views.list_all_books, name='books'),
    # Edit profile page
    url(r'^update-profile', user_views.update_profile, name='update-profile'),
    # Upload photo in profile edit page
    url(r'^upload-photo/(.+)$', user_views.upload_photo, name='upload_photo'),
    # Show profile photo
    url(r'^profile-photo/(.+)$', user_views.get_photo, name='photo'),
    url(r'^view-profile/(.+)$', user_views.view_profile, name='view-profile'),
]
