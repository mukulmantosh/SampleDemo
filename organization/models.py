from django.db import models
from django.contrib.auth.models import User
from . import constants


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Organization(TimestampModel):
    name = models.CharField(max_length=255)
    registration_code = models.CharField(max_length=50, unique=True)
    established_on = models.DateField()
    address = models.TextField(null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class BoardMembers(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, choices=constants.BOARD_MEMBERS)

    class Meta:
        verbose_name = "Board Member"
        verbose_name_plural = "Board Members"
