from django.shortcuts import render
from django.views import View
from django.http import  JsonResponse ,HttpResponse
from .forms import UserLoginForm , UsercreateForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import User , OtpCodeModel
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from random import randint
from utils.hash import hash_code
from utils.send_email import send_email_for_register,send_sms_for_login
from .models import QuestionModel
from django.contrib.auth.mixins import LoginRequiredMixin
from Orders.cart import Cart
from Category.models import CategoryModel
# Create your views here.
import time
from utils.utils import Is_Admin_User_Mixin
# Create your views here.

#نمایش صفحه لاگین و رجیستر 

# صفحات لاگین و رجیستر و کد و تغیر پسورد
class ShowFormLoginRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:#در صورتی که شخص لاگین باشد این صفحه نمایش داده نمیشود
            return redirect('Category:home')
        return super().dispatch(request, *args, **kwargs)

    def get(Self,request):
        cart=Cart(request)
        return render(request,'Accounts/login.html',{'cart':cart})
    



class LoginView(View):
    def post(self,request):
        
        form =UserLoginForm(request.POST)
        if form.is_valid():
            print('s'*999)
            cd = form.cleaned_data
            username = cd['username'].lower()
            password = cd['password']
            user = authenticate(request,username=username , password=password)
            if user is not None:
                otp_code = str(randint(10000,99999))
                # send_email_for_register(user.email,str(code))

                otp_model = OtpCodeModel.objects.filter(user=user)
               
                if otp_model.exists():
                    otp_model.delete()
                OtpCodeModel.objects.create(user=user,code=hash_code(otp_code))
                print(otp_code)
                request.session['user'] = {
                'email':username,
                'password':password,
                
            }
                return render(request,'Accounts/otpcode.html') #فرم به صورت اجکس نمایش داده میشود
                
            else:
                return JsonResponse({'status_login':'user_not_found'})
        else:
            return JsonResponse({'status_login':'form_not_valid'})





class OtpCodeView(View):
    def post(self,request):
        login_information =request.session['user'] #اطلاعات إخیره شده در فرم لاگین

        email= login_information['email']
        password = login_information['password']

        otp_code = request.POST['otp_code'] #کد نوشته شده توسط کاربر

        user = authenticate(request,username=email,password=password)
        
        otp_model = OtpCodeModel.objects.get(user=user)
        if str(otp_model.code) == hash_code(otp_code):
            otp_model.delete()
            login(request,user)
            return JsonResponse({'current_otp_code':True})
        return JsonResponse({'current_otp_code':False})




class RegisterView(View):
    def post(self,request):
        form = UsercreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email'].lower()
            username = cd['username'].lower()
            phone = cd['phone']
            password = cd['password']
            User.objects.create_user(email=email,username=username,phone=phone,password=password)
            return JsonResponse({'status_register':'user_register'})
        
        else:
            
            lst_err = list(form.errors.as_data().keys())
            return JsonResponse({'status_register':'form_error','error':lst_err})
            
           

class LogoutView(View):
    def get(self ,request):
        logout(request)
        messages.success(request,'شما با موفقیت خارج شدید','success')
        return redirect('Accounts:login_register')





class PasswordResetView(auth_view.PasswordResetView):
    template_name = 'Accounts/reset/password_reset.html'
    email_template_name = 'Accounts/reset/email.html'
    success_url=reverse_lazy('Accounts:password_reset_done')
    
    print(email_template_name)





class PasswordResetDoneView(auth_view.PasswordResetDoneView):
    print('9'*999)
    template_name = 'Accounts/reset/password_reset_done.html'




class PasswordResetConfirm(auth_view.PasswordResetConfirmView):
    template_name='Accounts/reset/password_reset_confirm.html'
    success_url=reverse_lazy('Accounts:password_reset_complate')
    


class PasswordResetComplateView(auth_view.PasswordResetCompleteView):
    template_name = 'Accounts/reset/password_reset_complate.html'





class ContactView(View):
    def get(self,request):
        cart=Cart(request)
        categories = CategoryModel.objects.all()
        all_like_me_count=0
        if request.user.is_authenticated:
            all_like_me_count = request.user.all_like_me_count()
        return render(request,'Accounts/contact_us.html',{'cart':cart,'len_cart':cart.get_len_cart,
                                                          'all_like_me_count':all_like_me_count,'categories':categories})
    def post(self,request):
        cd = request.POST
        name = cd['txt_name']
        que = cd['txt_question']
        QuestionModel.objects.create(name=name,que=que)
        messages.success(request,'سوال شما ثبت شد و در اسرع وقت به آن پاسخ داده میشود و در بخش سوالات به نمایش گداشته میشود ','success')
        return redirect('Accounts:contact')

class QuestionsView(View):
    def get(self,request):
        question = QuestionModel.objects.all()
        cart=Cart(request)
        categories = CategoryModel.objects.all()
        all_like_me_count=0
        if request.user.is_authenticated:
            all_like_me_count = request.user.all_like_me_count()
        return render(request,'Accounts/quastion.html',{'question':question,'len_cart':cart.get_len_cart,'all_like_me_count':all_like_me_count,'categories':categories})


class Answer_QuestionsView(Is_Admin_User_Mixin,View):
    def get(self,request):
        cart=Cart(request)
        categories = CategoryModel.objects.all()
        question = QuestionModel.objects.filter(answer__isnull=True)
        all_like_me_count=0
        if request.user.is_authenticated:
            all_like_me_count = request.user.all_like_me_count()
        return render(request,'Accounts/answer.html',{'question':question,'len_cart':cart.get_len_cart,'all_like_me_count':all_like_me_count,'categories':categories})
    def post(self,request):
        question =QuestionModel.objects.get(id= request.POST['id'])
        question.answer = request.POST['answer']
        question.save()
        return JsonResponse({'id':request.POST['id']})


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart(request)
        categories = CategoryModel.objects.all()
        all_like_me_count=0
        if request.user.is_authenticated:
            all_like_me_count = request.user.all_like_me_count()
        return render(request,'Accounts/profile.html',{'len_cart':cart.get_len_cart,'all_like_me_count':all_like_me_count,'categories':categories})
    
    def post(self,request):
        info = request.POST
        user = User.objects.get(id = request.user.id)
        try:
            name = info['txt_name'].split(' ')[0]
            family = ' '+info['txt_name'].split(' ')[1]
            user.name = name
            user.family = family
            user.username = info['txt_username']
            user.email = info['txt_email']
            user.phone = info['txt_phone']
            user.address = info['txt_address']
            img = request.FILES.get('img')
            if (img is not None):
                user.image = img
            
            user.save()
            if request.GET.get('next') =='orderview':
                return redirect('category:order')
            messages.success(request,'پروفایل شما با موفقیت تکمیل شد ','success')
            return redirect('Category:home')
        except:
            messages.success(request,'عملیات با خطا مواجه شد','success')
            return redirect('Accounts:profile')

        





class Check_Information_View(View):
    def post(self,request):
        txt_name = request.POST['txt_name']
        txt_value =  request.POST['txt_value']
        user=None
        if request.user.is_authenticated:
            user = User.objects.filter(**{txt_name:txt_value}).exclude(id = request.user.id).exists()
        else:
            user = User.objects.filter(**{txt_name:txt_value}).exists()
        # گرفتن یوزر
        if user:
            return JsonResponse({'status':False})
        return JsonResponse({'status':True})
        

        
            
        
           
            


































# class NotifacationView(View):
#     def get(self,request):
#         myorders = OrderModel.objects.filter(usersender=request.user,view=False)
#         # for order in myorders:
#         #     order.view = True
#         #     order.save
#         return render(request,'accounts/noti.html',{'myorders':myorders})
#     def post(self,request):
#         idorder = request.POST.get('idorder')
#         iduser = request.POST.get('iduser')






# class NotificationsView(View):
#     def get(self,request):
#         comments = ReplayCommentModel.objects.filter(to_user = request.user.username,view=False)
#         comments_tag = CommentModel.objects.filter(to_user = request.user.username)
        
#         comments_view = ReplayCommentModel.objects.filter(to_user = request.user.username,view=True)
#         return render(request,'accounts/notifications.html',{'comments':comments,'comments_view':comments_view,'comments_tag':comments_tag})
    
#     def post(self,request):
#         comments = ReplayCommentModel.objects.filter(to_user = request.user.username)
#         for c in comments:
#             c.view =True
#             c.save()
#         return JsonResponse({'status':'ok'})

