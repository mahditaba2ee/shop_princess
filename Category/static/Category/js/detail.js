
id_product = document.getElementById('id_product').dataset.id

// stars add and view 


function rank(rank,id,type_request){
    
    var datas = {'rank':rank,'id_product':id,'type_request':type_request} 
    request = create_request('/Option/rank',datas)
    request.onload=function()
    {
         const data = JSON.parse(this.responseText)
        if (data['status']=='user_not_login'){
            alert('برای ثبت نظر اول لاگین کنید')
        }
        else{
        var username = data['username']
        var rank =Number(data['rank'][username])
        for(i=1;i<=rank;i++){
            star=document.getElementById('star'+i)
            star.style.color='yellow'
        }
        var ranks = data['rank']
        var value_star = (Object.values(ranks))
        
        var avarage=0
        for(x in value_star){
            avarage+= Number(value_star[x])
        }
        avarage = avarage/value_star.length
        document.getElementById('avarage_rank').innerHTML=avarage.toFixed(1)
        document.getElementById('count_rank').innerHTML=`(${value_star.length}) بازخورد `
        for(i=1;i<=5;i++){
            var star = value_star.filter(x => x==i).length
            var width = String((star*100)/value_star.length)+'%'
            c= document.getElementById('rank'+i).style.width=width

        }
    }
    }
}

function star_mouse_move(btn,num){
    for(i=1;i<=5;i++){
        document.getElementById('star'+i).style.color='black'
    }
    for(i=1;i<=num;i++){
        document.getElementById('star'+i).style.color='yellow'
    }  
}


function star_mouse_leave(num){
    for(i=1;i<=num;i++){
        document.getElementById('star'+i).style.color='black'
        
    }
    
}

function star_mouse_click(btn){
    rank(btn.dataset.rank,btn.dataset.id,'add')
}

function star_box_leave(btn){
    
    rank(0,id_product,'start_page')
}




user_id=''
comment_id =''
function reply_icon_click(btn){
    
    comment_body.value='@'+btn.dataset.username+' '
    comment_id = btn.dataset.comment_id
    

}

function sumbit_comment(btn){

    datas={'comment_body':comment_body.value,'product_id':btn.dataset.product_id,'comment_id':comment_id}
    request = create_request('/Option/comment',datas,btn)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            btn.innerHTML="نظر"
            window.location.reload()
    
    }
    }
    
    
}





function sendproduct(btn){
    var id = btn.dataset.id
    txt = document.getElementById('product_number'+btn.dataset.id) 
    datas={}
    if(txt.value == 0){
        datas = {'id':btn.dataset.id ,'number':1}
    }
    if (txt.value > 0){
        datas = {'id':btn.dataset.id ,'type_request':'remove'}

    }

    request = create_request('/Orders/cart/add_and_remove',datas)
    request.onreadystatechange= function(){
        if(this.readyState==4){
            response = JSON.parse(this.responseText)
            if(response['cart_operation']=='remove'){
                product_add.classList.remove('text-danger')
                btn.dataset.status='buy'
                product_add_title.innerHTML='افزودن به کارت'
                txt.value=0
                

            }
            else{
                product_add.classList.add('text-danger')
                btn.dataset.status='sell'
                product_add_title.innerHTML="حذف از کارت"
                txt.value=1


        }
        len_cart.innerHTML=response['len_cart']
        // نوشته شدن کالا در کشو سبد خرید
        all_item_cart = create_request('/Orders/cart/list/item','')
        all_item_cart.onreadystatechange= function(){
            if(this.readyState==4){
                console.log(this.responseText);
                document.getElementById('all_cart_item').innerHTML=this.responseText
                
            }
        
        }
    }
}


    
}

rank(0,id_product,'start_page')