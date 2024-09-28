from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, role='user'):
        """
        Create and return a user with the given email, first name, last name, birthdate, and password.
        """
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, birthdate, password=None):
        """
        Create and return a superuser with the given email, first name, last name, birthdate, and password.
        """
        user = self.create_user(email, first_name, last_name, birthdate, password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Optional username
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # To determine if the user can access the admin site
    image=models.ImageField(upload_to='media/profile_images/', null=True, blank=True)

    # Setting email as the field used for login instead of the username
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
