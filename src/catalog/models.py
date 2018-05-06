import os
from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text


def section_upload_to(instance, filename):
    "Куда загружать картинки для разделов каталога"
    name, ext = os.path.splitext(filename)
    return force_text('sections/%s%s' % (uuid4(), ext.lower()))


def product_upload_to(instance, filename):
    "Куда загружать картинки для продуктов"
    name, ext = os.path.splitext(filename)
    return force_text('products/%s%s' % (uuid4(), ext.lower()))


class Section(models.Model):
    "Раздел каталога"
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=section_upload_to)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Product(models.Model):
    "Продукт"
    title = models.CharField(max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to=product_upload_to)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
