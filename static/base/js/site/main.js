loader.hidden=false
all_site.style.opacity='0'


document.getElementsByTagName('body')[0].style.overflowY= 'hidden';

function loaded_body(){
    loader.hidden=true
    all_site.style.opacity='1'
    document.getElementsByTagName('body')[0].style.overflowY= 'scroll';
}



(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    // Product Quantity
    // $('.quantity button').on('click', function () {
    //     var button = $(this);
    //     var oldValue = button.parent().parent().find('input').val();
    //     if (button.hasClass('btn-plus')) {
    //         var newVal = parseFloat(oldValue) + 1;
            
    //     } else {
    //         if (oldValue > 0) {
    //             var newVal = parseFloat(oldValue) - 1;
    //         } else {
    //             newVal = 0;
    //         }
    //     }
    //     button.parent().parent().find('input').val(newVal);
    // });
    
})(jQuery);

var box_top_sec = document.getElementById('box-top-sec')

window.onscroll = function(){
    if(document.documentElement.scrollTop>=50){
        box_top_sec.style.top=0
        box_top_sec.style.opacity='.8'
        box_top_sec.style.transition='1s'
    }
    else{
        box_top_sec.style.top='48px'
        box_top_sec.style.opacity='1'

    }
    hiden_kesho()

    // if(document.documentElement.scrollTop>=1100){
    //     div_product_sec.style.display='block'
    // }
    // else{
    //     div_product_sec.style.display='none'

    // }

};


function show_loading(){
    loader.hidden=false
    document.getElementsByTagName('body')[0].style.opacity='.5'
    document.getElementsByTagName('body')[0].style.overflowY= 'hidden';

}


function scrrol(){
    hiden_loading()
    $('html, body').animate({scrollTop: document.getElementById('product').offsetTop-150}, 2000, 'easeInOutExpo');
    return false;

}

function hiden_loading(){
    
    document.getElementsByTagName('body')[0].style.opacity='1'
    document.getElementsByTagName('body')[0].style.overflowY= 'scroll';
    loader.hidden=true
}























function menu_icon_click(btn){
    btn.style.transition= '.5s';
    if(btn.style.transform== 'rotate(180deg)'){
        
        btn.style.transform= 'rotate(-1deg)';
        return
    }
    
   
    btn.style.transform= 'rotate(180deg)';

    
    
}

function hiden_kesho_cart(close=false){
    if (close){
        nav_kesho_right.style.right='-2000px'
    }
    else{
        if(kesho.style.left=='0px'){
        
            kesho.style.left='-2000px'
        }
    nav_kesho_right.style.right='0'}

}
function show_div_hidden(){
    if(nav_kesho_right.style.right=='0px'){
        
        nav_kesho_right.style.right='-2000px'
    }
    kesho.style.left='0'

}
function hiden_kesho(){
 
    kesho.style.left='-2000px'

}
function type_show(btn){

    row = document.getElementById('type-category'+btn.dataset.id)
    if(row.style.height=='100%'){
        row.style.height='0'
        row.style.transform='scaleY(0)'
        for (let x = 0; x < row.children.length; x++) {
            const element = row.children[x];
            console.log(element);
            element.hidden=true
        }
    }
    else{
        row.style.height='100%'
        row.style.transform='scaleY(1)'
        for (let x = 0; x < row.children.length; x++) {
            const element = row.children[x];
            element.hidden=false
        }
    }
   
}



// hours=(new Date().getHours())
hours=true

function dark(){
//     if(document.getElementsByTagName('body')[0].classList=='night'){
//      document.getElementsByTagName('body')[0].style.backgroundImage='url(" https://beauty.s3.ir-thr-at1.arvanstorage.com/1.jpg")'
 
//      document.getElementsByTagName('body')[0].classList.remove('night')
 
//     }
//     else{
//      document.getElementsByTagName('body')[0].style.backgroundImage='url("")'
//      document.getElementsByTagName('body')[0].classList.add('night')
 
//  }
if(hours==false){
    document.getElementsByTagName('body')[0].style.backgroundImage='url("")'
    document.getElementsByTagName('body')[0].classList.add('night')

}
else{
    document.getElementsByTagName('body')[0].style.backgroundImage='url("https://beauty.s3.ir-thr-at1.arvanstorage.com/logo.jpg")'
 
    document.getElementsByTagName('body')[0].classList.remove('night')
}
 
 }
 dark()




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

// create request 

function create_request(url,datas,btn=null){

    const request = new XMLHttpRequest()
    request.onreadystatechange=function(){
        if(request.readyState==1){
            if(btn != null){
            btn.innerHTML='در حال بارگیری '
            }
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



function hiden_message_box(){
    setTimeout(function(){
        message_box.hidden=true
        
    },3000)
    
}
hiden_message_box()
// زمانی که مسیج از سرور میاد