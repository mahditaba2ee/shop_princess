from django.core.mail import send_mail
from django.conf import settings
from kavenegar import *
# from django.http import JsonResponse
# from django.views import View
# from .models import OrderItemsModel
# from Accounts.models import NotifacationModel
# class SendEmailView(View):
#     def post(self,request):
#         id = request.POST['iduser']
#         order_item=OrderItemsModel.objects.get(id = id)
#         name = order_item.product.name
#         order_id = order_item.order.id
#         email =  order_item.user_created.email
#         text =f"لطفا محصول {name} با کد سبد خریذ {order_id} را هر چه سریع تر تایید کنید "
#         send_mail('تاییدیه',text,settings.EMAIL_HOST_USER,(email,))

#         NotifacationModel.objects.create(user = order_item.user_created,text=text)

#         return JsonResponse({'status':email})





# def send_email(lst,id,email,address,name,family):
#     send_mail('تاییدیه',f'محصولات{lst}با کد{id}به آدرس {address}و مشخصات{name+family}ارسال شد با تشکر',settings.EMAIL_HOST_USER,(email,))
    
def send_email_for_register(email,txt):
    send_mail('کد ورود شما به سایت ',f'کد تایید شما {txt}میباشد لطفا کد را در اختیار کسی نگذارید',settings.EMAIL_HOST_USER,(email,))

def send_sms_for_login(sms='',txt=''):
    try:
        import json
    except ImportError:
        import simplejson as json
    try:
        api = KavenegarAPI('2F38694666396147696A4233696F4B767152754B57354C4B76724B6E2F324C6B7839694A58796F7A4F76593D')
        params = {
            'sender': '',
            'receptor' : '09134303981',
            'message' : "552255"
        }   
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)