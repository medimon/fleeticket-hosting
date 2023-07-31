from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, Group
from datetime import date
# from django import forms


class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        ('FR', 'FR'),
        ('DZ', 'DZ'),
    )
    role = models.CharField(max_length=2, choices=TYPE_CHOICES)


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('todo', 'Todo'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField(null=True, blank=True)
    # remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    deadline = models.CharField(max_length=20)
    userFr = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets_fr')
    userDz = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_dz')
    work = models.FileField(upload_to='uploads/', null=True)

    def __str__(self):
        return self.title

