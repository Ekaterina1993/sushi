from django.shortcuts import render
from catalog.models import Section


def index(request):
    "Главная страница"

    # все разделы каталога
    sections = Section.objects.all()

    # выводим через шаблон index.html
    return render(request, 'index.html', {'sections': sections})
