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
from memcpy import home_views, user_views

urlpatterns = [
    # The logged-in home page
    url(r'^$', home_views.logged_in_home, name='logged_in_home'),
    # Built-in authentication with our own template login page
    url(r'^login[/]?$', auth_views.login, {'template_name': 'memcpy/login.html'}, name='login'),
    # Logout a user and send them back to the login page
    url(r'^logout[/]?$', auth_views.logout_then_login, name='logout'),
    # User registration
    url(r'^register[/]?$', user_views.register, name='register'),
]
