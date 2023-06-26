function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
document.getElementById('nav-prodile').classList.add('active')

// create request 

function create_request(url,datas,btn=NaN){
    const request = new XMLHttpRequest()
    request.onreadystatechange=function(){
        if(request.readyState==1){
            btn.innerHTML='در حال بارگیری '

        }
        
    }
    const formdata = new FormData()
    request.open('POST',url)
    
    request.setRequestHeader('X-CSRFToken',csrftoken)
    var data;
    for (data in datas) {
        formdata.append(data,datas[data])

    }
    request.send(formdata)
    return request
}
function check_information(){
    var input_information= document.getElementsByClassName('information')
    
    for (let index = 0; index < input_information.length; index++) {
        const txt = input_information[index];
        
        change_txt(txt,txt.name)
        
    }

}
check_information()



function change_txt(txt,name){
    var regex=''
    
    if (name =='email'){
        regex = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
    }
    if(name =='name'|| name =='ostan' || name =='city' || name =='address'){
        if (txt.value.length<=2){
            txt.classList.remove('is-valid')
            txt.classList.add('is-invalid')
            txt.dataset.status='uncurrent'

            return
            
        }
        if(name =='address'){
            if (txt.value.length<=20){
                txt.classList.remove('is-valid')
                txt.classList.add('is-invalid')
            txt.dataset.status='uncurrent'

                alert('به نظر میرسد ادرس اشتباه است')
                return
                
            }
        }
        regex = new RegExp("[\u0600-\u06FF]");
    }
    if(name =='username'){
        regex = /^[a-zA-Z0-9]+$/;
    }
    if(name =='phone' ){
        regex = new RegExp("^(\\+98|0)?9\\d{9}$");
    }
    if(name=='codeposty'){
        regex = /\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b/gm;
    }

    if (regex.test(txt.value) === true) {
        txt.classList.remove('is-invalid')
        txt.classList.add('is-valid')
        txt.dataset.status='current'
    }
    else {
        txt.classList.remove('is-valid')
        txt.classList.add('is-invalid')
        txt.dataset.status='uncurrent'

    }
    
   
    
}



function order_click(){
    current_information = true
    var input_information = document.getElementsByClassName('information')
    for (let index = 0; index < input_information.length; index++) {
        
        const txt = input_information[index];
        if (txt.dataset.status=='uncurrent'){
            current_information=false
        }
        
    }
    if (current_information){
    message.hidden=true
    form = document.getElementById('form_information')
    
    var datas = {'fulname':txt_name.value,'email':txt_email.value,'phone':txt_phone.value,'ostan':txt_ostan.value
    ,'city':txt_city.value,'codepsty':txt_codeposty.value,'address':txt_address.value}
    request = create_request('/Orders/cart/checkout',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if(response['order_status'] == 'cart_null'){
                console.log(message);
                message.hidden=false
                message.innerHTML='سبد خرید شما خالی است'
            }
            if(response['order_status'] == 'input_null'){
                console.log(message);
                message.hidden=false
                message.innerHTML='اطلاعات  را تکمیل نمایید'
            }
            if(response['order_status'] == 'err'){
                console.log(message);
                message.hidden=false
                message.innerHTML='خطایی رخ داده است'
                }
            if(response['order_status'] == 'pay_online'){                
               window.location = '/Orders/order/pay'
            }
            if(response['order_status'] == 'pay_home'){
                window.location = '/Orders/order/pay/home'
             }
        }
        

    }
    

}
else{
   
    message.hidden=false
    message.innerHTML='اطلاعات  را به درستی تکمیل نمایید'
}

hiden_message()





}
function hiden_message(){
    setTimeout(function(){
        message.classList.remove('animate__fadeInRight')
        message.classList.add('animate__bounceOutLeft');
        message.addEventListener('animationend', () => {
            message.classList.remove('animate__bounceOutLeft');
            message.classList.remove('animate__fadeInRight')
            
            message.hidden=true
        })
    
    },5000)
    }






function printer(){
    window.print()
    }

   