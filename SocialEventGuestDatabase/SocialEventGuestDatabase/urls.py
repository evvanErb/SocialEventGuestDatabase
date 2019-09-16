"""SocialEventGuestDatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

import os

PATH = '/media/'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media'

from pages.views import homePage, passwordPreEnterGuest
from entries.views import enterGuest, retrieveGuest, guestCreated, retrievingGuest, errorPage

urlpatterns = [
    path('', homePage, name='homePage'),
    path('guestGu3sT6U3Sr/', enterGuest, name='enterGuest'),
    path('getThyGuest/', retrieveGuest, name='retrieveGuest'),
    path('guestCreated/', guestCreated, name='guestCreated'),
    path('passwordPreEnterGuest/', passwordPreEnterGuest, name='passwordPreEnterGuest'),
    path('retrievingGuest/', retrievingGuest, name='retrievingGuest'),
    path('errorPage/', errorPage, name='errorPage'),
    path('admin/', admin.site.urls),
]