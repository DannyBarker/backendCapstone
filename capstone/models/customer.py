from django.db import models
from django.contrib.auth.models import User
from .userType import UserType


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=55)
    city =  models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    zipcode = models.IntegerField()
    userType = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, related_name="category")

    # @property
    # def full_name(self):
    #     return f"{self.user.first_name} {self.user.last_name}"


    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")