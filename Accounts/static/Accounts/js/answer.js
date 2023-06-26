function answer(btn){
    row = document.getElementById('que_'+btn.dataset.id)
    txt_answer = document.getElementById('txt_que_'+btn.dataset.id).value
    datas = {'id':btn.dataset.id,'answer':txt_answer}
    request = create_request('/Accounts/answer',datas)
    request.onreadystatechange=function(){
        if(this.readyState==4){
            row.classList.add('animate__animated', 'animate__bounceOutLeft');
            row.addEventListener('animationend', () => {
                row.hidden=true
              });

        
    }}
}