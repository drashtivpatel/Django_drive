# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.BigIntegerField()
    profile_picture = models.ImageField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'profile_pictures',
                                                             'default-profile-img.png'))
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    # password = 'password'

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def check_password(self, raw_password):
        return self.password == raw_password


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    child_path = models.CharField(max_length=255)
    parent_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'files'), max_length=2048)
    original_path = models.CharField(default=os.path.join(os.getenv('HOME'), 'Drive_files', 'files'), max_length=2048)
    file_type = models.CharField(max_length=30)
    filename = models.CharField(max_length=1024)
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = 'file'
