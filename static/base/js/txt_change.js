function txt_change(txt,name){
   

    var regex;
    message = ''
    status_text=''
    if(name =='name'|| name =='ostan' || name =='city' || name =='address'){
        if (txt.value.length<=2){
            txt.classList.remove('is-valid')
            txt.classList.add('is-invalid')
            return
            
        }
        if(name =='address'){
            if (txt.value.length<=20){
                txt.classList.remove('is-valid')
                txt.classList.add('is-invalid')
                return
                
            }
        }
        regex = new RegExp("[\u0600-\u06FF]");
    }


    if(name =='phone'){
       
        regex = new RegExp("^(\\+98|0)?9\\d{9}$");
        message= 'شخص دیگری با این شماره ثبت نام کرده است'
        status_text='phone_status'
        
       
    }
    if (name =='email'){
        regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        message= 'شخص دیگری با این ایمیل ثبت نام کرده است'
        status_text='email_status'

    }
    if (name =='username'){
       
        if (txt.value.length>=5){
            regex = /^[a-zA-Z0-9]+$/;
            message= 'شخص دیگری با این نام کاربری ثبت نام کرده است'

        }
        else{
            
            txt.classList.add('invalid')
            return
            // تا زمانی که به 5 کلمه نرسد حلقه اجرا نمیشود
        }
}
if (name =='password'){
    if (txt.value.length>=8){
        txt.classList.remove('invalid')
        
        
    }
    else{
        
        txt.classList.add('invalid')
        
    }
    return
}
if (name =='repassword'){
    if (txt.value.length>=8){
       
        if(txt.value== id_new_password1.value){
            txt.classList.remove('invalid')
            
            return
        }
        else{
            
            txt.classList.add('invalid')
            


        }
    }
    else{
        txt.classList.add('invalid')
        return
    }
    return
}

        var result = regex.test(txt.value);
        if (result==false){
            
            txt.classList.add('invalid')
            
        }
      
        else{
            datas={'txt_value':txt.value,'txt_name':name}
            request = create_request('/Accounts/check/information/',datas)
            request.onreadystatechange=function(){
                if(this.readyState== 4){
                    response = JSON.parse(this.responseText)
                    
                    if(response["status"]==true){
                        txt.classList.remove('invalid')
                       
                      
                    }
                    else{
                        
                      
                        txt.classList.add('invalid')
                    }
                }
                
            }
            
         }

}


function txt_check_when_load_page(){
    var text_boxs= document.getElementsByClassName('user-information')
    for (let x = 0; x < text_boxs.length; x++) {
        const text_box = text_boxs[x];
        txt_change(text_box,text_box.name)

        
    }
}
