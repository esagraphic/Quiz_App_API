# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('account/', include('allauth.urls')),  # django-allauth routes
    path("", include("apps.authentication.urls")),  # Custom authentication routes
    path("", include("apps.home.urls")),  # Home app routes
]
