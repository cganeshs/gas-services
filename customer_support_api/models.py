from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")


class CustomAccountManager(BaseUserManager):
    def create_user(self,email,mobile_no,password,**other_fields):
        if not email:
            raise ValueError('Please provide an email address')
        email=self.normalize_email(email)
        user=self.model(email=email,mobile_no=mobile_no,**other_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,mobile_no,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)
        if other_fields.get('is_staff') is not True:
                raise ValueError('Please assign is_staff=True for superuser')
        if other_fields.get('is_superuser') is not True:
                raise ValueError('Please assign is_superuser=True for superuser')
        return self.create_user(email,mobile_no,password,**other_fields)


class Customer_Accounts(AbstractBaseUser,PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_accounts',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_accounts',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=13, unique=True, validators=[phone_validator])
    address = models.TextField(null=True)
    city = models.CharField(max_length=100,null=True)
    pincode = models.BigIntegerField(null=True)
    state = models.CharField(max_length=100,null=True)
    district = models.CharField(max_length=100,null=True)
    is_staff=models.BooleanField(default=False,null=True)
    is_active=models.BooleanField(default=True,null=True)
    is_admin = models.BooleanField(default=False,null=True)
    date_joined = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=["mobile_no",'full_name']

    class Meta:
        db_table = 'Customer_Accounts'

    def __str__(self):
        return self.email
    

class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer_Accounts, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=225)
    request_type = models.CharField(max_length=225)
    description = models.TextField()
    priority = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ServiceRequest'