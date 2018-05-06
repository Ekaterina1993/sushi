# coding: utf-8
import os
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

User = settings.AUTH_USER_MODEL


def upload_avatar(instance, filename):
    name, ext = os.path.splitext(filename)
    return force_text('users/avatars/%s%s' % (uuid4(), ext.lower()))


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        _('first name'), max_length=30, blank=True)
    last_name = models.CharField(
        _('last name'), max_length=150, blank=True)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    is_admin = models.BooleanField(
        default=False)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        default=True)
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now)
    avatar = models.ImageField(
        'Avatar', upload_to=upload_avatar, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, **kwargs):
        if self.pk:
            old = User.objects.get(pk=self.pk)
            if old.avatar != self.avatar:
                old.avatar.delete(False)
        super(User, self).save(**kwargs)

    def delete(self, **kwargs):
        self.avatar.delete(False)
        super(User, self).delete(**kwargs)
