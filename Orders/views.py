from django.shortcuts import render,redirect
from django.views import View
from .cart import Cart
from Category.models import ProductModel,CategoryModel
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import CoponModel,OrderItemsModel,OrderModel
import datetime
from utils.utils import copon_check , add_order,Is_Admin_User_Mixin
from utils.check_valid.check_information import check_phone ,check_codeposty 
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import requests
import json
import random
class CartView(View):
    # def dispatch(self, request, *args, **kwargs):
    #     cart = Cart(request)
    #     if cart.is_null():
    #         messages.success(request,'سبد خرید شما خالی است ','success') 
    #         return redirect('Category:home')  
    #     return super().dispatch(request, *args, **kwargs)
    def get(self,request):

       
        return render(request,'Orders/cart.html',{})

class Cart_Add_and_remove_View(View):
    def post(self,request):
        cart = Cart(request)
        post_price = cart.get_post_price('')
        product = ProductModel.objects.get(id=request.POST.get('id'))
        type_request = request.POST.get('type_request','add')
        if type_request == 'remove':
            cart.Remove(product)
            order_price=cart.get_order_price()
            
            len_cart = Cart(request).get_len_cart  
            return JsonResponse({'cart_operation':'remove','len_cart':len_cart,'order_price':order_price,'post_price':post_price})

        else:
            number = request.POST.get('number',1)
            cart.Add(product,number)
            order_price=cart.get_order_price()

            all_price_product = cart.get_all_price_product(product.id)
            len_cart = Cart(request).get_len_cart
            
            return JsonResponse({'cart_operation':'add','len_cart':len_cart,'all_price_product':all_price_product,'order_price':order_price,'post_price':post_price})

        
class Add_Product_To_Cart_Kesho(View):
    def post(self,request):
        cart = Cart(request)
        price=cart.get_order_price()
        return render(request,'Orders/cart_item_ajax.html',{'cart':cart})

class PayTypeView(View):
    def post(self,request):
        cart = Cart(request)
        pay_type = request.POST.get('pay_type','pay_online')
        request.session['pay_type'] = request.POST.get('pay_type','pay_online')
        return JsonResponse({'order_price':cart.get_order_price(),'post_price':cart.get_post_price(pay_type),'order_price':cart.get_order_price()})
   

class CoponView(View):
    def post(self,request):       
        copon_code = request.POST.get('copon_code')
        copon_valid=copon_check(request,copon_code)
        request.session['off_per']=copon_valid
        return JsonResponse({'copon_check':copon_valid})
       



class CheckOutView(View):
    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        if cart.is_null():
            messages.success(request,'سبد خرید شما خالی است ','success') 
            return redirect('Category:home')  
        per_off = request.session.get('off_per',None)
        if per_off is None:
            per_off=0
        
        self.pay_type = request.session['pay_type']
        self.cart=cart
        self.price_post=cart.get_post_price(self.pay_type)
        self.order_price = cart.get_order_price()
        self.get_price_with_off=cart.get_price_with_off(per_off)
        self.get_order_price_with_post_price=cart.get_order_price_with_post_price(self.pay_type,per_off)
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        categories = CategoryModel.objects.all()
        all_like_me_count=0
        if request.user.is_authenticated:
            all_like_me_count = request.user.all_like_me_count()
        return render(request,'Orders/checkout.html',{'post_price':self.price_post,
        'order_price':self.order_price,'order_price_with_off':int(self.get_price_with_off),
        'get_order_price_with_post_price':int(self.get_order_price_with_post_price),'pay_type':self.pay_type})


    def post(self,request):
        cd = request.POST
        current_information=True
        cart =self.cart
        if cart.is_null()==False:
            if(cd['fulname'] != '' and cd['address']!='' and cd['phone']!='' and cd['ostan']!='' and cd['city']!='' and cd['codepsty']!=''):
                


                if (check_phone(cd['phone']) ):
                    request.session['information_order'] = {
                    
                    'fulname':cd['fulname'],
                    'email':cd['email'],
                    'address':cd['address'],
                    'phone':cd['phone'],
                    'ostan':cd['ostan'],
                    'city':cd['city'],
                    'codepsty':cd['codepsty']
                    }
                    if (self.pay_type =='pay_home'):
                        return JsonResponse({'order_status':'pay_home'})
                    else: 
                        return JsonResponse({'order_status':'pay_online'})
                else:
                    return JsonResponse({'order_status':'err'})


            else:
                return JsonResponse({'order_status':'input_null'})
        else:
            return JsonResponse({'order_status':'cart_null'})







class OrderView(Is_Admin_User_Mixin,View):
    
    def get(self,request):
        self.orders = OrderModel.objects.filter(view=False)
        search = request.GET.get('search')
        orders = self.orders
        if search:
            orders =self.orders.filter(Q(id__contains=search)|Q(phone__contains=search))
       
        return render (request,'Orders/Orders.html',{'orders':orders})

    def post(self,request):
        order_id = request.POST.get('order_id',None)
        if order_id:
            order = OrderModel.objects.get(id=order_id)
            order.view=True
            order.user_view=request.user
            order.save()
            return JsonResponse({'status_order':'order_view'})
        return JsonResponse({'status_order':'err'})

class Archive_Order_view(Is_Admin_User_Mixin,View):
   
    def get(self,request):
        self.orders = OrderModel.objects.filter(view=True)
        search = request.GET.get('search')
        orders = self.orders
        if search:
            orders =self.orders.filter(Q(id__contains=search)|Q(phone__contains=search))
        return render (request,'Orders/Orders.html',{'orders':orders})

    def post(self,request):
        order_id = request.POST.get('order_id',None)
        if order_id:
            order = OrderModel.objects.get(id=order_id)
            order.view=True
            order.save()
            return JsonResponse({'status_order':'order_view'})
        return JsonResponse({'status_order':'err'})



if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'



ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
phone = '09133655315'
CallbackURL = 'http://127.0.0.1:8000/Orders/verify_pay'
class OrderPayView(View):
    def get(self,request):
       
        pay_type = request.session['pay_type']
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount":int(Cart(request).get_order_price_with_post_price(pay_type)),
        "Description": description,
        "Phone": '09133655315',
        "CallbackURL": CallbackURL,
    }
        data = json.dumps(data)
    # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            
            response1 = requests.post(ZP_API_REQUEST, data=data,headers=headers ,timeout=10)
            
            if response1.status_code == 200:
                response1 = response1.json()
                authority=(response1['Authority'])
                if response1['Status'] == 100:
                    
                    return  redirect(ZP_API_STARTPAY + str(response1['Authority']) )
                    
                else:
                    return {'status': False, 'code': str(response1['Status'])}
            return response1
    
        except requests.exceptions.Timeout:
            return render(request,'inc/error.html')
        except requests.exceptions.ConnectionError:
            return render(request,'inc/error.html',{'err':'internet'})





class VerifyPayView(View):
    def get(self,request):
        authority = request.GET['Authority']
        pay_type = request.session['pay_type']

        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(Cart(request).get_order_price_with_post_price(pay_type)),
        "Authority": authority,
    }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response1 = requests.post(ZP_API_VERIFY, data=data,headers=headers)
        if response1.status_code == 200:
            response = response1.json()
            if response['Status'] == 100:
                order_add=add_order(request,response['RefID'])
                if (order_add==True):
                    return render(request,'inc/success.html',{'RefID':response['RefID']})
                else:
                    return render(request,'inc/error.html',{'err':'cancel'})
            else:
                return render(request,'inc/error.html',{'err':'cancel'})
        return render(request,'inc/error.html')

class OrderPayHomeViwe(View):
    def get(self,request):
        RefID = random.randint(1000000,9999999) 
        order_add=add_order(request,RefID)
        if (order_add==True):
                    return render(request,'inc/success.html',{'RefID':RefID})
        else:
            return render(request,'inc/error.html',{'err':'cancel'})