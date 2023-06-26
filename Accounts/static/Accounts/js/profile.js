

 
nav_prodile.classList.add('active')



function change_profile(){
    (change_img.files[0].name)
    var r = new FileReader()
    r.readAsDataURL(change_img.files[0])
    r.onload =function(e){
        const result = e.target.result;
        profile_img1.src = result
        // request = create_request('/Accounts/changeprofileimage',{'src':result})
        // request.onreadystatechange=function(){
        //     if (this.readyState==4){
        //         alert('ssss')
        //     }
        // }
    }
}
txt_check_when_load_page()




