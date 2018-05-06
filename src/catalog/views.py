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
from django.shortcuts import get_object_or_404

from .models import Section

# Create your views here.

def view_section(request, section_slug):
    "Промотр раздела каталога"
    section = get_object_or_404(Section, slug=section_slug)
    products = section.products.all()

    return render(request, 'catalog/view_section.html', {'section': section, 'products': products})