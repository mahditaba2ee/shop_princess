
from django import forms
from .models import User
from utils.check_valid.check_information import Check_Email,check_username ,check_phone
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UsercreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,required=False)
    repassword = forms.CharField(widget=forms.PasswordInput,required=False)

    class Meta:
        model = User
        fields = ('email','username','phone')
    
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password !=repassword:
            raise forms.ValidationError('password not math')
        if len(repassword) < 7:
            raise forms.ValidationError('password not 8 ')
        return repassword
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('email airly exist')
        if Check_Email(email):
            return email
        raise forms.ValidationError('email airly exist')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError('username airly exist')
        if check_username(username):
            return username
        raise forms.ValidationError('username airly exist')
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone=phone).exists()
        if user==False:
            if check_phone(phone):
                return phone
        raise forms.ValidationError('phone airly exist','ss')
        
    
    def save(self, commit= False):
        print('g'*90)
        print(commit)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
