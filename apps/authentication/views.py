# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from allauth.account.utils import send_email_confirmation
from allauth.account.views import ConfirmEmailView
from django.http import HttpResponseRedirect
from django.urls import reverse


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        # Render a custom confirmation page with a button
        return render(request, "account/email_confirm.html", {"key": kwargs.get("key")})

    def post(self, request, *args, **kwargs):
        # Process the confirmation when the button is clicked
        response = super().post(request, *args, **kwargs)
        messages.success(request, "Your email has been successfully confirmed. You can now log in.")
        return redirect("login/")  # Redirect to the login page


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/app/subject-list/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive
            user.save()
            send_email_confirmation(request, user)  # Send email confirmation
            msg = "A confirmation email has been sent to your email address."
            success = True
        else:
            msg = "Form is not valid"
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
