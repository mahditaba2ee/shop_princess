


change_category(category_option.value)

function change_category(value){
        
        if(value=='add'){
            window.location='/category/addcategory'
        }
        if(value=='none'){
            return
        }

        else{
        while(brand_option.hasChildNodes()){
            brand_option.removeChild(brand_option.firstChild);
        }
        while(type_option.hasChildNodes()){
            type_option.removeChild(type_option.firstChild);
        }

        datas ={'id':value}
        request = create_request('/Category/choise',datas)
        request.onreadystatechange=function(){
            if(this.readyState==4){
                response = JSON.parse(this.responseText)
                type_lst=response['type_lst'];
                brand_lst = response['brand_lst']
                
                for (type in type_lst) {
                    type_option.add(new Option(type_lst[type],type));
                }
                for (brand in brand_lst) {
                    console.log(brand);
                    brand_option.add(new Option(brand_lst[brand],brand));
                }
               
            }
        }

    

       
                
            }
    }

function add_product(){
    images=[]
    form = document.getElementById('form_add_product')
    var datas = {'name':form['txt_name'].value,'email':form['txt_email'].value,'phone':form['txt_phone'].value,'password1':form['txt_password1'].value
    ,'password2':form['txt_password2'].value}
    

    
    request = create_request('/add',datas)
    request.onreadystatechange=function(){
        
            console.log(this.responseText);
        
    }
}



