document.getElementById('nav-type').classList.add('active')


var id_btn = 0
function type_product_click(btn , page=1,order='name'){
    loader.hidden=false
    document.getElementsByTagName('body')[0].style.opacity='.5'
    document.getElementsByTagName('body')[0].style.overflowY= 'hidden';
        id_btn = btn
        const request = new XMLHttpRequest()
        
        request.open('GET','/type/products/?type='+btn.dataset.id + '&page='+page+'&order='+order )
        request.onreadystatechange=function(){
            if (this.readyState != 4){
                loader.hidden=true
                document.getElementsByTagName('body')[0].style.opacity='1'
                document.getElementsByTagName('body')[0].style.overflowY= "scroll";

            }
                document.getElementById('product').innerHTML = this.responseText  
                
        }
        request.send()
    
    
    
    
}

$('.show-type').click(function () {
    $('html, body').animate({scrollTop: document.getElementById('show-type').offsetTop}, 2000, 'easeInOutExpo');
    return false;
});





order = 'name'
function page_click(btn){
    $('html, body').animate({scrollTop: document.getElementById('show-type').offsetTop-150}, 2000, 'easeInOutExpo');
    
    type_product_click(id_btn,btn.dataset.num,order,'page_click')
    return false;
}

function oreder_change(value){
    type_product_click(id_btn,1,value)
    order = value
}