# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),  # django-allauth routes  # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE

    # Leave `Home.Urls` as last the last line
    path("app/", include("apps.home.urls")),
    path("", include("landing.urls"))
]  
if settings.DEBUG is True:
    urlpatterns += path(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path(settings.STATIC_URL, document_root=settings.STATIC_ROOT)