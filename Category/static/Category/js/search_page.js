lists = document.querySelectorAll('.list')
body_1.style.height='100vh'
for (let i = 0; i < lists.length; i++) {
    lists[i].classList.remove('active');
    
}
li = document.getElementById('list-search')
li.classList.add('active')
function search_click(){
    box.style.top='70px'
    box.style.position='fixed';
    
    $.get("/home/card", function(data, status){
        products.innerHTML=data
        body_1.style.height='100%'
        
    });
  
}