from django.contrib import admin
from django.contrib.admin.sites import site
from .models import *
# Register your models here.
admin.site.register(CatName)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(HomeBanner)
admin.site.register(Coupon)
admin.site.register(QaA)
admin.site.register(ReturnsPolicy)
admin.site.register(ShippingPolicy)
admin.site.register(TermsCondition)
