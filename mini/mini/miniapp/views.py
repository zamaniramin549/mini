from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import secrets

# Stripe
import stripe
stripe.api_key = "sk_test_f5DFxUlH8kcahbSOsJy8m0SL00GyZrj6kY"

import datetime
from .models import *
from miniadmin.models import *
# Create your views here.


def home(request):

    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None

    banners = HomeBanner.objects.all().order_by('-pk')
    category = CatName.objects.all().order_by('cat_name')

    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product


    return render(request, 'index.html',{
        'category':category,
        'product':product,
        'banners':banners,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
    })


def shop(request):

    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None


    category = CatName.objects.all().order_by('cat_name')
    product = Product.objects.all().order_by('-pk')
    product_img = ProductImage.objects.all()

    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product

    return render(request, 'shop.html',{
        'category':category,
        'product':product,
        'product_img':product_img,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
    })


def product_detail(request, pk):

    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None


    productOne = Product.objects.get(pk = pk)

    product = Product.objects.all()
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')


    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product

    category = CatName.objects.get(pk = productOne.cat)
    product_img = ProductImage.objects.filter(product_pk = pk)
    return render(request, 'product_detail.html',{
        'category':category,
        'productOne':productOne,
        'product_img':product_img,
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
    })


def add_to_cart(request):
    if request.user.is_authenticated:


        if request.method == 'POST' and 'add' in request.POST:
            get_product_id = request.POST.get('product_id')
            quantity = Product.objects.get(pk = get_product_id).stuck
            if Product.objects.get(pk = get_product_id).stuck >= 1:
                if len(Cart.objects.filter(product_pk = get_product_id,user_pk = request.user.pk)) == 1:
                    get_product = Cart.objects.get(product_pk = get_product_id,user_pk = request.user.pk)
                    get_product.quantity = get_product.quantity + 1
                    get_product.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    add = Cart(
                        product_pk = get_product_id,
                        quantity = 1,
                        user_pk = request.user.pk,
                    )
                    add.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        if request.method == 'POST' and 'add_to_cart_2' in request.POST:
            get_product_id_2 = request.POST.get('product_id')
            quantity = request.POST.get('num-product')
            if int(quantity) != 0:
                if Product.objects.get(pk = get_product_id_2).stuck >= 1 and int(quantity) <= Product.objects.get(pk = get_product_id_2).stuck:
                    if len(Cart.objects.filter(product_pk = get_product_id_2,user_pk = request.user.pk)) == 1:
                        get_product = Cart.objects.get(product_pk = get_product_id_2,user_pk = request.user.pk)
                        get_product.quantity = get_product.quantity + int(quantity)
                        get_product.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        add = Cart(
                            product_pk = get_product_id_2,
                            quantity = int(quantity),
                            user_pk = request.user.pk,
                        )
                        add.save()
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return redirect('/')


def viewcart(request):
    if request.user.is_authenticated:
        msgw = None
        get_code = None
        dis = None
        add_on = None
        try:
            user_info = UserInfo.objects.get(user_pk = request.user.pk)
        except:
            user_info= None

        product = Product.objects.all().order_by('-pk')
        user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
        user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

        total = 0
        subtotal = 0
        for count in user_cart_products:
            for product_price in product:
                if count.product_pk == product_price.pk:
                    one_product = count.quantity * product_price.price
                    subtotal = subtotal + one_product
                    add_on = ((subtotal + one_product) * 1.7) / 100
                    total = subtotal + add_on

        if request.method == 'GET' and 'coupon_apply' in request.GET:
            today = datetime.date.today()
            get_code = request.GET.get('coupon')
            if len(Coupon.objects.filter(name = get_code)) == 1:
                get_coupon = Coupon.objects.get(name = get_code)
                if get_coupon.expiry >= today:
                    dis = (total * int(get_coupon.descount)) / 100
                    total = total - dis
                else:
                    msgw = f'{get_code} is expired.'
            else:
                msgw = f'The coupon code does not exist.'


    else:
        return redirect('/')
    return render(request, 'viewcart.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'msgw':msgw,
        'get_code':get_code,
        'subtotal':subtotal,
        'add_on':add_on,
        'dis':dis,
    })


def payment(request):
    if request.user.is_authenticated:
        subtotal = 0
        if request.method == 'POST':
            country = request.POST.get('country')
            state = request.POST.get('state')
            address = request.POST.get('address')
            postcode = request.POST.get('postcode')
            countrycode = request.POST.get('country_code')
            phone = request.POST.get('phone')
            total = request.POST.get('total')
            token = request.POST.get('stripeToken')
            customre = stripe.Customer.create(
                    email = request.user.username,
                    name = request.user.first_name + ' ' + request.user.last_name,
                    source = token,
                )
            stripe.Charge.create(
                customer = customre,
                amount= int(total) * 100,
                currency="myr",
                description= 'Mini Hair Care',
            )
            today = datetime.date.today()
            product = Product.objects.all().order_by('-pk')
            user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')
            unique_id = secrets.token_hex(100)
            create_date = DatePurchase(
                    user_pk = request.user.pk,
                    date = today,
                    view = 'notyet',
                    amount = int(total),
                    country = country,
                    state = state,
                    address = address,
                    postcode = postcode,
                    countrycode = countrycode,
                    tell = phone,
                    unique_id = unique_id
                )
            create_date.save()
            for cart in user_cart_products:
                for products in product:
                    if products.stuck >= cart.quantity and cart.product_pk == products.pk:
                        get_date_purchase = DatePurchase.objects.get(user_pk = request.user.pk, unique_id = unique_id).pk
                        save_product = Purchases(
                                user_pk = request.user.pk,
                                product_pk = cart.product_pk,
                                date_purchase_pk = get_date_purchase,
                                quantity = cart.quantity,
                            )
                        save_product.save()
                        get_product = Product.objects.get(pk = products.pk)
                        get_product.stuck = get_product.stuck - cart.quantity
                        get_product.save()
                        get_cart_to_delete = Cart.objects.filter(pk = cart.pk)
                        get_cart_to_delete.delete()
                    else:
                        pass
                
            return redirect('viewcart')
    else:
        return redirect('/')


def add_more(request, pk):
    if request.user.is_authenticated:
        get_cart = Cart.objects.get(pk = pk, user_pk = request.user.pk)
        get_product_stuck = Product.objects.get(pk = get_cart.product_pk) 
        if get_product_stuck.stuck > get_cart.quantity:
            get_cart.quantity = get_cart.quantity + 1
            get_cart.save()
            return redirect('viewcart')
        else:
            return redirect('viewcart')
    else:
        return redirect('/')


def reduce(request, pk):
    if request.user.is_authenticated:
        get_cart = Cart.objects.get(pk = pk, user_pk = request.user.pk)
        if get_cart.quantity != 1:
            get_cart.quantity = get_cart.quantity - 1
            get_cart.save()
            return redirect('viewcart')
        else:
            return redirect('viewcart')
    else:
        return redirect('/')


def remove(request, pk):
    if request.user.is_authenticated:
        get_cart = Cart.objects.filter(pk = pk, user_pk = request.user.pk)
        get_cart.delete()
        return redirect('viewcart')
    else:
        return redirect('/')


def phistory(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
        product = Product.objects.all().order_by('-pk')
        user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
        user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

        total = 0
        for count in user_cart_products:
            for product_price in product:
                if count.product_pk == product_price.pk:
                    one_product = count.quantity * product_price.price
                    total = total + one_product

        history_date = DatePurchase.objects.filter(user_pk = request.user.pk).order_by('-pk')
        # history_product = Purchases.objects.filter(user_pk = request.user.pk)
    else:
        return redirect('/')
    return render(request, 'phistory.html',{
        'user_info':user_info,
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'history_date':history_date,
    })
    

def viewproducts_user(request, pk):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
        product = Product.objects.all().order_by('-pk')
        user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
        user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

        total = 0
        for count in user_cart_products:
            for product_price in product:
                if count.product_pk == product_price.pk:
                    one_product = count.quantity * product_price.price
                    total = total + one_product

        history_date = DatePurchase.objects.get(user_pk = request.user.pk, pk= pk)
        history_product = Purchases.objects.filter(date_purchase_pk = pk , user_pk = request.user.pk)
    else:
        return redirect('/')
    return render(request, 'viewproducts.html',{
        'user_info':user_info,
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'history_date':history_date,
        'history_product':history_product,
    })


def qa(request):
    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None
    qnas = QaA.objects.all()
    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product


    return render(request, 'Q&A.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'qnas':qnas,
    })


def returnspolicy(request):
    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None
    returnpolicy = ReturnsPolicy.objects.get(pk = 1)
    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product


    return render(request, 'returnspolicy.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'returnpolicy':returnpolicy,
    })


def shippingpolicy(request):
    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None
    returnpolicy = ShippingPolicy.objects.get(pk = 1)
    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product


    return render(request, 'shippingpolicy.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'returnpolicy':returnpolicy,
    })


def termscondition(request):
    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None
    returnpolicy = TermsCondition.objects.get(pk = 1)
    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product


    return render(request, 'termscondition.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'returnpolicy':returnpolicy,
    })


def contact(request):
    msg = None
    msgw = None
    try:
        user_info = UserInfo.objects.get(user_pk = request.user.pk)
    except:
        user_info= None
    product = Product.objects.all().order_by('-pk')
    user_cart_count = Cart.objects.filter(user_pk = request.user.pk).count
    user_cart_products = Cart.objects.filter(user_pk = request.user.pk).order_by('-pk')

    total = 0
    for count in user_cart_products:
        for product_price in product:
            if count.product_pk == product_price.pk:
                one_product = count.quantity * product_price.price
                total = total + one_product

    if request.method == 'POST' and 'send' in request.POST:
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        if email != '' and msg != '':
            savemsg = Msgs(
                email = email,
                content = msg
            )
            savemsg.save()
            msg = 'Thanks for contacting us. We will respont as soon as posible.'
        else:
            msgw = 'Both Email and your message is required.'


    return render(request, 'contact.html',{
        'product':product,
        'user_cart_count':user_cart_count,
        'user_cart_products':user_cart_products,
        'total':total,
        'user_info':user_info,
        'msg':msg,
        'msgw':msgw,
    })


def loginuser(request):
    if not request.user.is_authenticated:
        msgw = None
        if request.method == 'POST' and 'loginbtn' in request.POST:
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            user_authenticate = authenticate(username = email, password = password)
            if user_authenticate != None:
                login(request, user_authenticate)
                return redirect('/')
            else:
                msgw = 'Your email or password is wrong.'
    else:
        return redirect('/')
    return render(request, 'loginuser.html',{
        'msgw':msgw,
    })


def register(request):
    if not request.user.is_authenticated:
        msgw = None
        fname = None
        lname = None
        email = None
        msg = None
        if request.method == 'POST' and 'registerbtn' in request.POST:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email').lower()
            password = request.POST.get('password')
            password_two = request.POST.get('password_two')
            terms = request.POST.get('terms')
            if terms == 'accepted':
                if len(User.objects.filter(username = email)) == 0:
                    if password == password_two:
                        create_user = User.objects.create_user(
                            username = email,
                            email = email,
                            password = password_two,
                            first_name = fname,
                            last_name = lname,
                        )
                        create_user.save()
                        get_for_userinfo = User.objects.get(username = email).pk
                        add_user_info = UserInfo(
                            permission = 'user',
                            user_pk = get_for_userinfo,
                            terms = terms
                        )
                        add_user_info.save()
                        msg = 'Registration was successful.'
                    else:
                        msgw = 'Passwords aren\'t match.'
                else:
                    msgw = f'{email} is already exist.'
            else:
                msgw = 'You have to accept our terms and condition.'
    else:
        return redirect('/')
    return render(request, 'register.html',{
        'msgw':msgw,
        'fname':fname,
        'lname':lname,
        'email':email,
        'msg':msg,
    })


def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return render('/')