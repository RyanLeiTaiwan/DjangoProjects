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
from django.conf.urls import url, include
from django.contrib import admin
from memcpy import home_views

urlpatterns = [
    # Django admin console
    url(r'^admin[/]?', admin.site.urls),
    # The non-logged-in home page
    url(r'^$', home_views.non_logged_in_home, name='non_logged_in_home'),
    # Include another URLconf
    url(r'^memcpy/', include('memcpy.urls')),
]

handler404 = 'memcpy.misc_views.custom_404'
