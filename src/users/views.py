# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from . import forms


@login_required
def change_password(request):
    if request.method == 'POST':
        form = forms.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Success')
            return redirect('user:profile')
    else:
        form = forms.PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def profile(request):

    if request.method == 'POST':

        form = forms.UserProfileForm(
            request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            prof = form.save(commit=False)
            prof.save()
            messages.success(request, 'Success')
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = forms.UserProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile': request.user})


def signup(request):

    if request.method == "POST":
        form = forms.RegistrationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.last_login = datetime.now()
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            auth_login(request, new_user)
            return redirect('/')
    else:

        form = forms.RegistrationForm

    return render(request, 'users/signup.html', {'form': form})


class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm


class LogoutView(auth_views.LogoutView):
    next_page = '/'
