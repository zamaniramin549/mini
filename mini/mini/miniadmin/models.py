from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.http import request

# Create your models here.
class CatName(models.Model):
    cat_name = models.CharField(max_length=255)
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    cat          = models.IntegerField(null=True, blank=True)
    img          = models.FileField(null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    price        = models.IntegerField(null=True, blank=True)
    description  = models.TextField(null=True, blank=True)
    video        = models.CharField(max_length=255,null=True, blank=True)
    stuck        = models.IntegerField()
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    image = models.FileField(null=True, blank=True)
    product_pk = models.IntegerField(blank=True, null=True)
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    

class HomeBanner(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)
    banner = models.FileField(null=True, blank=True)
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    

class Coupon(models.Model):
    name = models.CharField(max_length=255)
    expiry = models.DateField()
    descount = models.IntegerField()
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class QaA(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user_pk = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class ReturnsPolicy(models.Model):
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

class ShippingPolicy(models.Model):
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

class TermsCondition(models.Model):
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)