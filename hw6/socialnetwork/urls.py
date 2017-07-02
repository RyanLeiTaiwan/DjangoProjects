"""socialnetwork URL Configuration

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
from socialnetwork import views as sn_views

urlpatterns = [
    # The home page
    url(r'^$', sn_views.index, name='index'),
    # Built-in authentication with our own template login page
    url(r'^login[/]?$', auth_views.login, {'template_name': 'socialnetwork/login.html'}, name='login'),
    # Logout a user and send them back to the login page
    url(r'^logout[/]?$', auth_views.logout_then_login, name='logout'),
    # User registration
    url(r'^register[/]?$', sn_views.register, name='register'),
    # View profile
    url(r'^profile/(?P<user_id>[0-9]+)[/]?$', sn_views.profile, name='profile'),
    # Post a message
    url(r'^post[/]?$', sn_views.post, name='post'),
    # Edit profile
    url(r'^edit/(?P<user_id>[0-9]+)[/]?$', sn_views.edit, name='edit'),
    # Return a profile picture
    url(r'^profile/(?P<user_id>[0-9]+)/pic[/]?$', sn_views.get_picture, name='picture'),
    # Following stream
    url(r'^following[/]?$', sn_views.following_stream, name='following_stream'),
    # Follow a user
    url(r'^follow/(?P<user_id>[0-9]+)[/]?$', sn_views.follow, name='follow'),
    # Unfollow a user
    url(r'^unfollow/(?P<user_id>[0-9]+)[/]?$', sn_views.unfollow, name='unfollow'),
    # Get posts using AJAX
    url(r'^get-posts-comments/(?P<user_id>[-]?[0-9]+)[/]?$', sn_views.get_posts_comments, name='get-posts'),
    # Add a comment
    url(r'^comment/(?P<post_id>[0-9]+)/(?P<param_user_id>[-]?[0-9]+)?$', sn_views.comment, name='comment'),
]
