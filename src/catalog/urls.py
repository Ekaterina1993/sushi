from django.urls import path

from . import views

urlpatterns = [
     path('<slug:section_slug>/', views.view_section, name='view_section'),
]
