"""Models for Hypoxic Admin"""
import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class HypoxicUserManager(BaseUserManager):
    """User Management Model"""
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin_user(self, email, password):
        """
        Creates and saves an admin user with the given email and
        password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class HypoxicUser(AbstractBaseUser):
    """User Model"""
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    objects = HypoxicUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
