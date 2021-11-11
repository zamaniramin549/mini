from django.urls import path
from miniadmin import views
urlpatterns = [
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('viewproducts/', views.viewproducts, name='viewproducts'),
    path('homebanner/', views.homebanner, name='homebanner'),
    path('coupon/', views.coupon, name='coupon'),
    path('adminpurchases/', views.adminpurchases, name='adminpurchases'),
    path('edit_pro/<int:pk>/', views.edit_pro, name='edit_pro'),
    path('view_purchases/<int:pk>/', views.view_purchases, name='view_purchases'),
    path('qna/', views.qna, name='qna'),
    path('viewadminqna/', views.viewadminqna, name='viewadminqna'),
    path('returnspolicyadmin/', views.returnspolicyadmin, name='returnspolicyadmin'),
    path('shippingpolicyadmin/', views.shippingpolicyadmin, name='shippingpolicyadmin'),
    path('temrsadmin/', views.temrsadmin, name='temrsadmin'),
    path('messages/', views.messages, name='messages'),
]