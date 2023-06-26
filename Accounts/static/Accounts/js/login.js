lists = document.querySelectorAll('.list')
for (let i = 0; i < lists.length; i++) {
    lists[i].classList.remove('active');
    
}
li = document.getElementById('list-login')
li.classList.add('active')


function show_other_form(){
    if (frm_register.style.display=='none'){
    box_form.style.height='650px'
    frm_register.style.display='block'
    frm_login.style.display='none'
}

else{
    
    box_form.style.height='420px'
    frm_login.style.display='block'
    frm_register.style.display='none'

}
}

function login(btn){

    
    const username =txt_username.value
    const password =txt_password.value
    const datas = {'username':username,'password':password}
    var request= create_request('/Accounts/login',datas,btn)
    // اسال درخواست با اجکس به سمت سرور
    request.onreadystatechange=function(){
        
        if(this.readyState==4)
            {

                btn.innerHTML='ورود'
            try{
               
                response = JSON.parse(this.responseText)
                

                if (response['status_login'] == 'user_not_found'){
                    message_text.innerHTML=' نام کاربری یا رمز عبور صحیح نمیباشد'
                    show_message()
                }
                if(response['status_login']=='form_not_valid'){ 
                    message_text.innerHTML='مقادیر را برراسی کنید'
                    show_message()
                
                }
        }
        // در صورتی که در سرور json برنگردد اجرا
        catch{
            box_form.innerHTML=this.responseText;   
            }
        
    }
 

}


}
function otpcode_btn_click(btn){


    otp_code = txt_otpcode.value
    var datas = {'otp_code':otp_code}
    var request = create_request('/Accounts/verify_otp_code',datas,btn)
    request.onreadystatechange=function(){
       
        if(this.readyState==4){
            btn.innerHTML='ورود'
            response = JSON.parse(this.responseText)
            if(response['current_otp_code']==true){
                location.reload()
            }
            if(response['current_otp_code']==false){
                
                message_text.innerHTML='کد نامعتبر است '
                show_message()
            }
        }
    }

}

function register_click(btn){
    // واکشی اطلاعات فرم رجیستر
    form = form_register
    var datas = {'username':form['username'].value,'email':form['email'].value,'phone':form['phone'].value,'password':form['password'].value
    ,'repassword':form['repassword'].value}

    var request=create_request('/Accounts/register',datas,btn)
    request.onreadystatechange=function(){
        
        if(this.readyState==4){
        response = JSON.parse(this.responseText);
        btn.innerHTML='ثبت نام'
        // بررسی ارور ها و نمایش آن به کاربر در حال ثبت نام
        if (response['status_register'] == 'form_error'){
            message_box.hidden=false
            message_box.innerHTML='موارد زیر را بررسی کنید'
        }
       
        if (response['status_register'] == 'user_register'){
            message_box.hidden=false
            message_box.innerHTML='تبریک! شما ثبت نام شده اید لطفا وارد شوید'
            text_boxs = document.getElementsByClassName('user-information')
            for (let x = 0; x < text_boxs.length; x++) {
                const text_box = text_boxs[x];
                text_box.value=''
            }
            
        }
        
    }




    }
    hiden_message_box()

}







