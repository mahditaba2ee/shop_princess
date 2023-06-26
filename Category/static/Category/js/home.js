window.onscroll = function(){
    if(document.documentElement.scrollTop>=50){
        box_top_sec.style.top=0
        box_top_sec.style.opacity='.8'
        box_top_sec.style.transition='1s'
    }
    else{
        box_top_sec.style.top='38px'
        box_top_sec.style.opacity='1'

    }
    hiden_kesho()

};


function helo_click(){
    let client = new coreapi.Client();
    let schema = null;
    client.get("http://127.0.0.1:8000/").then(function(data) {
        // Load a CoreJSON API schema.
        schema = data;
        console.log('schema loaded');
    })
}


slug = ''
function category_search(btn=null,cat_slug='',page=1){
   
    const request = new XMLHttpRequest()
    
    if (cat_slug != ''){
        slug = cat_slug

    }
    else{
        slug = btn.dataset.slug
    }
    request.open('GET','/search/'+slug+'/?is_ajax=true&page='+page)
    request.onreadystatechange=function(){
        if (this.readyState != 4){
            
        }
        else{
            
            div_remove = document.getElementsByClassName('remove')
            for (let x = 0; x < div_remove.length; x++) {
             const element = div_remove[x];
             element.innerHTML=''
             element.style.display='none'
            }
                scrrol()
                title_product.innerHTML=slug
                product.innerHTML = this.responseText  
                
        }
       
    }
    request.send()
 
}

function page_click(btn){
    // پیدا کردن تایل کتگوری
    cat_slug=document.getElementById('category_slug').dataset.category_slug
    category_search(null,cat_slug,btn.dataset.num)

}


function comment_for_site(){
    message_box.hidden=false
    message_box.innerHTML='نظر شما در مورد سایت ثبت شد .'
    my_inerval = setInterval(() => {

        message_box.hidden=true
        clearInterval(my_inerval)


    
    }, (5000));
}




function setting_slide(btn){
    window.location='add_slide?id_slide='+btn.dataset.id
}



