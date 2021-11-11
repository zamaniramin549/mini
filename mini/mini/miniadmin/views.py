import os
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import datetime
from .models import *
from miniapp.models import *
# Create your views here.
def adminpanel(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            today = datetime.date.today()
            amonth_ago = today - datetime.timedelta(30)
            sixmonth_ago = today - datetime.timedelta(180)


            last_30_days = DatePurchase.objects.filter(date__range=[amonth_ago, today])
            total = 0
            for count in last_30_days:
                total = total + count.amount

            last_6_months = DatePurchase.objects.filter(date__range=[sixmonth_ago, today])
            total_six = 0
            for count_six in last_6_months:
                total_six = total_six + count_six.amount

            total_today = 0
            today_earnings = DatePurchase.objects.filter(date = today)
            for count_today in today_earnings:
                total_today = total_today + count_today.amount

            all_time = 0
            total_earnings =  DatePurchase.objects.all()
            for all in total_earnings:
                all_time = all_time + all.amount

            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            total_orders = DatePurchase.objects.all().count

            all_products = Product.objects.all().count
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'dashboard.html',{
        'user_type':user_type,
        'total':total,
        'total_today':total_today,
        'total_six':total_six,
        'all_time':all_time,
        'new_orders':new_orders,
        'total_orders':total_orders,
        'all_products':all_products,
    })


# Purchases
def adminpurchases(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            date_purchases = DatePurchase.objects.all().order_by('-pk')
            users = User.objects.all()
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'adminpurchases.html',{
        'user_type':user_type,
        'date_purchases':date_purchases,
        'users':users,
        'new_orders':new_orders,
    })



# Vew Purchases
def view_purchases(request, pk):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            date_purchase = DatePurchase.objects.get(pk = pk)
            user = User.objects.get(pk = date_purchase.user_pk)
            products = Purchases.objects.filter(date_purchase_pk = pk)
            all_products = Product.objects.all()
            date_purchase.view = 'yes'
            date_purchase.save()
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'view_purchases.html',{
        'user_type':user_type,
        'date_purchase':date_purchase,
        'products':products,
        'user':user,
        'all_products':all_products,
        'new_orders':new_orders,
    })


    
# Add category
def addcategory(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            msg = None
            msgw = None
            category = CatName.objects.all().order_by('-pk')

            if request.method == 'POST' and 'save_cat' in request.POST:
                cat_name = request.POST.get('cat_name').lower()
                if len(CatName.objects.filter(cat_name = cat_name)) == 0:
                    save_cat = CatName(
                        cat_name = cat_name,
                        user_pk = request.user.pk
                    )
                    save_cat.save()
                    msg = f'{cat_name} save successfully.'
                else:
                    msgw = f'{cat_name} already exist.'

            if request.method == 'POST' and 'save_cat_name' in request.POST:
                cat_name_change = request.POST.get('cat_name_change').lower()
                cat_pk = request.POST.get('cat_pk')
                if len(CatName.objects.filter(cat_name = cat_name_change)) == 0:
                    change_name = CatName.objects.get(pk = cat_pk)
                    change_name.cat_name = cat_name_change
                    change_name.save()
                    msg = f'Category successfully updated to {cat_name_change}.'
                else:
                    msgw = f'{cat_name_change} already exist.'

            if request.method == 'POST' and 'del_cat' in request.POST:
                cat_pk_del = request.POST.get('cat_pk_del')
                get_cat = CatName.objects.filter(pk = cat_pk_del)
                get_cat.delete()
                msg = f'Category deleted successfully.'
              
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'addcategory.html',{
        'user_type':user_type,
        'category':category,
        'msg':msg,
        'msgw':msgw,
        'new_orders':new_orders,
    })

# Add product
def addproduct(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            catgory = CatName.objects.all().order_by('cat_name')
            msg = None
            msgw = None
            product_name = None
            product_price = None
            description = None
            video = None
            stuck = None
            if request.method == 'POST' and 'save_product' in request.POST:
                category = request.POST.get('category')
                product_name = request.POST.get('product_name').lower()
                product_price = request.POST.get('product_price')
                stuck = request.POST.get('stuck')
                image = request.FILES.getlist('product_image')
                image_two = request.FILES['thumbnail']
                fs = FileSystemStorage()
                filename = fs.save(image_two.name, image_two)
                image_two = fs.url(filename)
                description = request.POST.get('description')
                video = request.POST.get('video')
                if category != 'None':
                    save_product = Product(
                        img = image_two,
                        cat = category,
                        product_name = product_name,
                        price = product_price,
                        description = description,
                        stuck = stuck,
                        video = video,
                        user_pk = request.user.pk
                    )
                    save_product.save()
                    get_product = Product.objects.get(cat = category,product_name = product_name,price = product_price,description = description,video = video,user_pk = request.user.pk, stuck=stuck).pk
                    for images in image:
                        save_image = ProductImage(
                            image = images,
                            product_pk = get_product,
                            user_pk = request.user.pk
                        )
                        save_image.save()
                    msg = f'{product_name} added successfully.'
                else:
                    msgw = f'Please select a category for the product.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'addproduct.html',{
        'user_type':user_type,
        'catgory':catgory,
        'msg':msg,
        'msgw':msgw,
        'product_name':product_name,
        'product_price':product_price,
        'description':description,
        'video':video,
        'stuck':stuck,
        'new_orders':new_orders,
    })

# View Products
def viewproducts(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            msg = None
            msgw = None
            product = Product.objects.all().order_by('-pk')
            cat = CatName.objects.all()
            if request.method == 'POST' and 'add_on' in request.POST:
                get_stuck = request.POST.get('get_stuck')
                get_stuck = int(get_stuck)
                stuck_pk = request.POST.get('stuck_pk')
                if get_stuck >= 1:
                    get_product = Product.objects.get(pk = stuck_pk)
                    get_product.stuck = get_stuck
                    get_product.save()
                    msg = f'You have added {get_stuck} to stuck.'
                else:
                    msgw = f'The stuck should be more than 1.'

            if request.method == 'POST' and 'del_pro' in request.POST:
                pro_pk_del = request.POST.get('pro_pk_del')
                get_pro = Product.objects.filter(pk = pro_pk_del)
                get_pro_image = ProductImage.objects.filter(product_pk = pro_pk_del)
                for del_image in get_pro_image:
                    del_img = ProductImage.objects.get(pk = del_image.pk)
                    os.remove(del_img.image.path)
                get_pro.delete()
                get_pro_image.delete()
                msg = f'Product deleted successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'viewproducts_admin.html',{
        'user_type':user_type,
        'product':product,
        'msg':msg,
        'msgw':msgw,
        'cat':cat,
        'new_orders':new_orders,
    })

# Edit product
def edit_pro(request, pk):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            msg = None
            product = Product.objects.get(pk = pk)
            get_cat = CatName.objects.get(pk = product.cat)
            product_img = ProductImage.objects.filter(product_pk = pk)
            catgory = CatName.objects.all().order_by('cat_name')
            if request.method == 'POST' and 'del_img' in request.POST:
                del_img = request.POST.get('img_pk')
                get_img_to_del = ProductImage.objects.get(pk = del_img)
                os.remove(get_img_to_del.image.path)
                get_img_to_del.delete()
                msg = 'Image deleted successfully.'

            if request.method == 'POST' and 'save_product' in request.POST:
                category = request.POST.get('category')
                product_name = request.POST.get('product_name').lower()
                product_price = request.POST.get('product_price')
                stuck = request.POST.get('stuck')
                image = request.FILES.getlist('product_image')
                description = request.POST.get('description')
                video = request.POST.get('video')
                try:
                    image_two = request.FILES['thumbnail']
                    fs = FileSystemStorage()
                    filename = fs.save(image_two.name, image_two)
                    image_two = fs.url(filename)

                    get_product = Product.objects.get(pk = pk)
                    get_product.cat = category
                    get_product.product_name = product_name
                    get_product.price = product_price
                    get_product.img = image_two
                    get_product.description = description
                    get_product.video = video
                    get_product.stuck = stuck
                    get_product.save()
                    for images in image:
                        save_image = ProductImage(
                            image = images,
                            product_pk = pk,
                            user_pk = request.user.pk
                        )
                        save_image.save()
                    msg = f'{product_name} updated successfully.'
                except:
                    get_product = Product.objects.get(pk = pk)
                    get_product.cat = category
                    get_product.product_name = product_name
                    get_product.price = product_price
                    get_product.description = description
                    get_product.video = video
                    get_product.stuck = stuck
                    get_product.save()
                    for images in image:
                        save_image = ProductImage(
                            image = images,
                            product_pk = pk,
                            user_pk = request.user.pk
                        )
                        save_image.save()
                    msg = f'{product_name} updated successfully.'
                    
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'edit_pro.html',{
        'user_type':user_type,
        'product':product,
        'product_img':product_img,
        'get_cat':get_cat,
        'catgory':catgory,
        'msg':msg,
        'new_orders':new_orders,
    })

# Home banner
def homebanner(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            msg = None
            msgw = None
            get_banners = HomeBanner.objects.all().order_by('-pk')
            if request.method == 'POST' and 'save_banner' in request.POST:
                title = request.POST.get('title').lower()
                season = request.POST.get('season').lower()
                image_two = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(image_two.name, image_two)
                image_two = fs.url(filename)
                if len(HomeBanner.objects.filter(title = title)) == 0:
                    save_banner = HomeBanner(
                        title = title,
                        season = season,
                        banner = image_two,
                        user_pk = request.user.pk
                    )
                    save_banner.save()
                    msg = f'{title} added successfully.'
                else:
                    msgw = f'{title} is already exist. Please choose new title.'
            if request.method == 'POST' and 'banner_pk' in request.POST:
                banner = request.POST.get('banner_pk')
                get_banner = HomeBanner.objects.get(pk = banner)
                # os.remove(get_banner.banner.path)
                get_banner.delete()
                msg = 'Banner romeved successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'homebanner.html',{
        'user_type':user_type,
        'get_banners':get_banners,
        'msg':msg,
        'msgw':msgw,
        'new_orders':new_orders,
    })


# Q&A
def qna(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            msg = None
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            if request.method == 'POST' and 'save' in request.POST:
                title = request.POST.get('title')
                description = request.POST.get('description')
                save_q = QaA(
                    title = title,
                    description = description,
                    user_pk = request.user.pk
                )
                save_q.save()
                msg = f'{title} added to Q&A successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'qna.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'msg':msg,
    })


# View Q&A
def viewadminqna(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            msg = None
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            qnas = QaA.objects.all().order_by('-pk')
            if request.method == 'POST' and 'save_edited_qnas' in request.POST:
                title = request.POST.get('qnas_title_2')
                description = request.POST.get('des')
                qna_pk = request.POST.get('qnas_pk')
                qna = QaA.objects.get(pk = qna_pk)
                qna.title = title
                qna.description = description
                qna.save()
                msg = f'{title} updated successfully,'
            if request.method == 'POST' and 'del_qnas' in request.POST:
                get_pk  = request.POST.get('qnas_pk_del')
                get_qna = QaA.objects.filter(pk = get_pk)
                get_qna.delete()
                msg = 'Delete was successful.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'viewadminqna.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'qnas':qnas,
        'msg':msg,
    })


# Return Policy
def returnspolicyadmin(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            msg = None
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            retunrspolicy = ReturnsPolicy.objects.get(pk = 1)
            if request.method == 'POST' and 'save' in request.POST:
                content = request.POST.get('content')
                retunrspolicy.content = content
                retunrspolicy.save()
                msg = 'Returns Policy updated successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'returnspolicyadmin.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'retunrspolicy':retunrspolicy,
        'msg':msg,
    })

# Shipping Policy
def shippingpolicyadmin(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            msg = None
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            retunrspolicy = ShippingPolicy.objects.get(pk = 1)
            if request.method == 'POST' and 'save' in request.POST:
                content = request.POST.get('content')
                retunrspolicy.content = content
                retunrspolicy.save()
                msg = 'Shipping Policy updated successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'shippingpolicyadmin.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'retunrspolicy':retunrspolicy,
        'msg':msg,
    })

# Terms and condition
def temrsadmin(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            msg = None
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            retunrspolicy = TermsCondition.objects.get(pk = 1)
            if request.method == 'POST' and 'save' in request.POST:
                content = request.POST.get('content')
                retunrspolicy.content = content
                retunrspolicy.save()
                msg = 'Terms & Condition updated successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'temrsadmin.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'retunrspolicy':retunrspolicy,
        'msg':msg,
    })


# Messages
def messages(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            messages = Msgs.objects.all().order_by('-pk')
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'messages.html',{
        'user_type':user_type,
        'new_orders':new_orders,
        'messages':messages,
    })

# coupon
def coupon(request):
    if request.user.is_authenticated:
        user_type = UserInfo.objects.get(user_pk = request.user.pk)
        if user_type.permission == 'superuser':
            new_orders = DatePurchase.objects.filter(view = 'notyet').count
            msg = None
            msgw = None
            coupon = Coupon.objects.all().order_by('-pk')
            if request.method == 'POST' and 'save_coupon' in request.POST:
                name = request.POST.get('coupon_name')
                date = request.POST.get('date')
                discount = request.POST.get('discount')
                if len(Coupon.objects.filter(name = name)) == 0:
                    save_coupon = Coupon(
                        name = name,
                        expiry = date,
                        descount = discount,
                        user_pk = request.user.pk
                    )
                    save_coupon.save()
                    msg = f'{name} added successfully.'
            if request.method == 'POST' and 'save_edited_coupon' in request.POST:
                name_2 = request.POST.get('coupon_name_2')
                coupom_pk = request.POST.get('coupon_pk')
                discount = request.POST.get('discount')
                try:
                    date_2 = request.POST.get('date_2')
                    get_coupon  = Coupon.objects.get(pk = coupom_pk)
                    get_coupon.name = name_2
                    get_coupon.expiry = date_2
                    get_coupon.descount = discount
                    get_coupon.save()
                    msg = 'Coupon updated successfully.'
                except:
                    get_coupon  = Coupon.objects.get(pk = coupom_pk)
                    get_coupon.name = name_2
                    get_coupon.descount = discount
                    get_coupon.save()
                    msg = 'Coupon updated successfully.'

            if request.method == 'POST' and 'del_coupon' in request.POST:
                coupon_pk = request.POST.get('coupon_pk_del')
                get_coupon_to_delete = Coupon.objects.filter(pk = coupon_pk)
                get_coupon_to_delete.delete()
                msg = 'Coupon deleted successfully.'
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'coupon.html',{
        'user_type':user_type,
        'msg':msg,
        'coupon':coupon,
        'msgw':msgw,
        'new_orders':new_orders,
    })