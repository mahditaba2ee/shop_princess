from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.http import HttpRequest, HttpResponse, JsonResponse
from Product_option.models import CommentModel,ReplayCommentModel
from utils.utils import shopping_cart,page,filtering,Is_Admin_User_Mixin
from Orders.cart import Cart
from .forms import AddProductForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# @method_decorator(cache_page(5*60),name='dispatch')
class CategoryView(View):
    def dispatch(self, request, *args, **kwargs):
        self.products = ProductModel.objects.filter(available=True)
        self.slids_images = ImagdeSlidModel.objects.all()[:5]
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
      
        most_like_product = self.products[:8] 
        off_product = self.products.filter(special=True)[:8]
        return render(request,'Category/home.html',{'page':'home','most_like_product':most_like_product,
        'off_product':off_product,'slids_images':self.slids_images})
        
class SearchView(View):
    
    def get(self,request):
      
        return render(request,'Category/search_page.html')
        


class ProductDetailsView(View):

    def get(self,request,*args,**kwargs): 
        product = ProductModel.objects.get(slug=kwargs['product_slug'])
        similar_products = ProductModel.objects.filter(type=product.type)
        comments = CommentModel.objects.filter(product=product)
        buys = []
        if request.session.get('cart') is not None:
            buys = shopping_cart(request)
        # دریافت تعداد محصولات موجود در سبد برای نشان دادن در صفحه توضیحات
        number=0
        if product.id in buys:
            id_product = str(product.id)
            number = request.session['cart'][id_product]['number']
        return render(request,'Category/detail.html',{'product':product,'simiar_products':similar_products,'comments':comments,'number':number})
# @method_decorator(cache_page(5*60),name='dispatch')
class SearchCategoryView(View):
    def dispatch(self, request, *args, **kwargs):
        self.category = CategoryModel.objects.get(slug=kwargs['category_slug'])
        self.products = ProductModel.objects.filter(category = self.category)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,category_slug,type_slug=None,name_product=None,search=None):
        search_name_product=self.category.name
        order = request.GET.get('order','name')
        page_type = ''
        type_slug_select=None
        p = request.GET.get('page',1) 
        lst_name = TypeProductModel.objects.filter(category = self.category)
        page_type= 'category_search'
        if type_slug:
            type = TypeProductModel.objects.get(slug = type_slug)
            search_name_product=type.name
            type_slug_select = type.slug
            self.products=self.products.filter(type=type)
            lst_name = set(name.name for name in type.product_to_type.all() )
            page_type= 'type_search'
        if name_product:
            self.products = self.products.filter(name=name_product)
            search_name_product=name_product
        if search:
            self.products=self.products.filter(name__contains = search)
        
        order_convert_to_farsi={
            'name':'نام',
            '-like_count':"بیشترین لایک",
            'all_price':" ارزانترین",
            '-all_price':"گرانترین",
            "created":"جدیدترین",
            "name":"نام"
        }.get(order,'noting')

        self.products=page(self.products.order_by(order),p)
        if request.GET.get('is_ajax'):
            return render(request,'Category/shop_ajax.html',{"products":self.products,'p':int(p)})
        
        return render(request,'Category/category_search.html',{"products":self.products,'type_slug_select':type_slug_select,
        'p':int(p),'lst_product':lst_name,'page_type':page_type,'order_convert_to_farsi':order_convert_to_farsi,'search_name_product':search_name_product,'order':order})


class BoxSearchView(View):
    def get(Self,request,text_search):
        p = request.GET.get('page',1)
        order = request.GET.get('order','name')
        products=page(ProductModel.objects.filter(full_name__contains = text_search).order_by(order),p)
        order_convert_to_farsi={
            'name':'نام',
            '-like_count':"بیشترین لایک",
            'all_price':" ارزانترین",
            '-all_price':"گرانترین",
            "created":"جدیدترین",
            "name":"نام"
        }.get(order,'noting')
        
        return render(request,'Category/category_search.html',{"products":products,'text_search':text_search,'order_convert_to_farsi':order_convert_to_farsi,'order':order,'p':int(p),'page_type':'text_search'})


class ShopView(View):
    def dispatch(self, request, *args, **kwargs):
        self.categories = CategoryModel.objects.all()
        self.brands = BrandModel.objects.all()
        self.products = ProductModel.objects.all().order_by('created')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        is_ajax = request.GET.get('ajax',False)
        page_number = request.GET.get('page',1)
        order = request.GET.get('order','name')
        if is_ajax ==False:
            products = page(self.products,page_number)
            return render(request,'Category/shop.html',{'brands':self.brands,'products':products,'p':int(page_number)})
        if is_ajax:
            products = filtering(request,self.products.order_by(order))
            products=page(products,page_number)
            
            
            return render(request,'Category/shop_ajax.html',{'products':products,'p':int(page_number)})

     



class TypeProductView(View):
    def get(self,request):
        type_id = request.GET.get('type',False)
        order = request.GET.get('order','name')
       
        if type_id:
            type = TypeProductModel.objects.get(id = type_id)  
            products= ProductModel.objects.filter(type = type).order_by(order)
            p = request.GET.get('page',1)
            products = page(products,p)
            return render(request,'Category/shop_ajax.html',{'products':products,'p':int(p),'page_type':'type_list'})
        typies = TypeProductModel.objects.all()
        return render(request,'Category/list_type.html',{'typies':typies})




class LikeCategoryView(LoginRequiredMixin,View):
        
    def get(self,request):       
        products = ProductModel.objects.filter(like = request.user)
        return render(request,'Category/category_search.html',{"products":products})



# بیشتریین بازدید که url در فوتر میباشد
class Most_View(View):
    def dispatch(self, request, *args, **kwargs):
        self.products = ProductModel.objects.all()[:8]
        return super().dispatch(request, *args, **kwargs)
    def get(self,request): 
        p = request.GET.get('page',1)
        buys = shopping_cart(request)         
        products=page(self.products,p)
        return render(request,'Category/category_search.html',{"products":products,'buys':buys,'p':int(p)})



# class SeeMoreView(View):
#     def get(self,request):
#         order = request.GET.get('see')
#         products = ProductModel.objects.all().order_by(order)
#         products=page(products,1)
#         return render(request,'Category/category_search.html',{"products":products})

        
class Add_Slide_View(Is_Admin_User_Mixin,View):
    
    def get(self,request):
        id_slide=request.GET.get('id_slide',False)
        if id_slide:
            slide = ImagdeSlidModel.objects.get(id = id_slide)
            return render(request,'Category/Add_slide.html',{'slide':slide})
        return render(request,'Category/Add_slide.html')
        
    def post(self,request):
        cd = request.POST
        id_slide=request.GET.get('id_slide',False)
        img = request.FILES.get('img')
        if img is None:
            messages.info(request,'عکسی را انتخاب کنید','info')
            return redirect('Category:add_slide')
        url=cd['txt_url']
        title=cd['txt_title']
        des=cd['txt_des']
        if id_slide:
            slide = ImagdeSlidModel.objects.get(id = id_slide)
            slide.title=title
            slide.des=des
            slide.url=url
            slide.image=img
            slide.save()
            messages.success(request,'ویرایش انجام شد','success')
            return redirect('Category:add_slide')
       
        ImagdeSlidModel.objects.create(image=img,url=url,title=title,des=des)
        messages.success(request,'اسلاید اضافه شد','success')
        return redirect('Category:add_slide')
        




class AddProductView(Is_Admin_User_Mixin,View):
    def get(self,request):
        brands = BrandModel.objects.all()
        type = TypeProductModel.objects.all()
        return render(request,'Category/add_product.html',{'brands':brands,'type':type})
  
    def post(self,request):
        brand_id=request.POST['brand_option']
        type_id = request.POST['type_option']
        category_id = request.POST['category_option']
        form =AddProductForm(request.POST)
        category = CategoryModel.objects.get(id=category_id)
        brand = BrandModel.objects.get(category=category,id =brand_id )
        type = TypeProductModel.objects.get(id=type_id )
       
        if form.is_valid():
                
                cd = form.cleaned_data
                product = ProductModel.objects.create(name=cd['name'],full_name=cd['full_name'],des=cd['des'],all_price=cd['all_price'],off_price=cd['off_price'] ,
                category=category,brand=brand,type=type)              
                product.save()
                
        file = request.FILES.getlist("images[]")
            
        for img in file:
                ImageProductModel.objects.create(product=product,image=img)
        messages.success(request,'کالا اضافه شد','success')
        return redirect('Category:add_product')

        
       



     
class ChoiseView(View):
    
    def post(self,request):
        id = request.POST['id']
        print('ssss'*90)
        print(id)
        category = CategoryModel.objects.get(id=id)
        typies = TypeProductModel.objects.filter(category=category)
        brands = BrandModel.objects.filter(category=category)
        brand_lst={}
        type_lst={}
        for brand in brands:
            brand_lst[brand.id]=brand.name
        for type in typies:
            type_lst[type.id]=type.name
        
        return JsonResponse({'brand_lst':brand_lst,'type_lst':type_lst})


