from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateField

# Create your models here.
class UserInfo(models.Model):
    permission = models.CharField(max_length=255, default='user')
    user_pk    = models.IntegerField()
    img        = models.FileField(null=True, blank=True)
    terms      = models.CharField(max_length=255)
    date       = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    product_pk   = models.IntegerField()
    user_pk      = models.IntegerField()
    quantity     = models.IntegerField()
    date    = models.DateTimeField(auto_now_add=True)


class DatePurchase(models.Model):
    user_pk = models.IntegerField()
    date = models.DateField()
    view = models.CharField(max_length=255, default='notyet')
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=255)
    countrycode = models.CharField(max_length=255)
    tell = models.CharField(max_length=255)
    amount = models.IntegerField()
    unique_id = models.CharField(max_length=255)


class Purchases(models.Model):
    user_pk = models.IntegerField()
    product_pk = models.IntegerField()
    date_purchase_pk = models.IntegerField()
    quantity = models.IntegerField()
    date    = models.DateTimeField(auto_now_add=True)

class Msgs(models.Model):
    email = models.EmailField()
    content = models.TextField()
    status = models.CharField(max_length=20, default='unread')
    date = models.DateTimeField(auto_now_add=True)