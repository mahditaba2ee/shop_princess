

// در نوابار دکمه ورود رنگش عوض میشود
nav_lagin.classList.add('active')  


function login_click(btn){
    message_box.hidden=true
    const email = txt_email.value
    const password =txt_password.value
    const datas = {'email':email,'password':password}
    var request= create_request('/Accounts/login',datas,btn)
    // اسال درخواست با اجکس به سمت سرور
    request.onreadystatechange=function(){
        
        if(this.readyState==4)
            {

                btn.innerHTML='ورود'
            try{
               
                response = JSON.parse(this.responseText)
                message_box.hidden=false

                if (response['status_login'] == 'user_not_found'){
                    message_box.innerHTML=' نام کاربری یا رمز عبور صحیح نمیباشد'
                    
                }
                if(response['status_login']=='form_not_valid'){ 
                    message_box.innerHTML='لطفا مقادیر را بررسی کنید'
                
                }
        }
        // در صورتی که در سرور json برنگردد اجرا
        catch{
            main.innerHTML=this.responseText;   
            }
        
    }
 

}
hiden_message_box()


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

txt_check_when_load_page()