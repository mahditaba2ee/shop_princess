from django.core.paginator import Paginator
from Orders.models import CoponModel , OrderItemsModel , OrderModel
from Orders.cart import Cart 
from Category.models import ProductModel
import datetime
from django.contrib.auth.mixins import UserPassesTestMixin 
def shopping_cart(request):
    buys=[]
    if request.session.get('cart') is not None:
        for product_id in list(request.session['cart'].keys()):
                    buys.append(int(product_id))
    return buys


def page(products,page_number):
    paginator = Paginator(products,8)
    page_number = page_number
    page_obj =paginator.get_page(page_number)
    return page_obj


def filtering (request,quety_product):
        products=[]
        
        prices = request.GET.get('lst_price','')
        brands = request.GET.get('lst_brand','')
        categories = request.GET.get('lst_categories','')
        
        if prices != '' or brands!='' or categories!='' :
            prices = prices.split(',')
            brands = brands.split(',')
            categories = categories.split(',')
            
            if prices!=['']:
                    
                for price in prices:
                    
                    if price == '1':
                        for p in quety_product:
                            if p.all_price >=0 and p.all_price<=20000:
                                products.append(p)
                    if price == '2':
                        for p in quety_product:
                            if p.all_price >20000 and p.all_price<=50000:
                                products.append(p)
                    if price == '3':
                        for p in quety_product:
                            if p.all_price >50000 and p.all_price<=80000:
                                products.append(p)
                    if price == '4':
                        for p in quety_product:
                            if p.all_price >80000:
                                products.append(p)
            else:
                products = quety_product
            
            brand_product=[]
            if brands!=['']:   
                for p in products:  
                    if str(p.brand.id) in brands:
                        brand_product.append(p)
                else:
                    products=[] 
            if brand_product !=[]:
                products=brand_product
            cat_product=[]
            if categories!=['']:       
                for p in products:
                    if str(p.category.id) in categories:
                         cat_product.append(p)
                else:
                    products=[]
            if cat_product:
                products=cat_product
           
            return products
        return quety_product
def copon_check(request,copon_code):
   
   
    copon_code = copon_code
    copon_model = CoponModel.objects.filter(end__gte=datetime.datetime.now())
    for c in copon_model:
        if c.copon_code == copon_code:
            if request.user in c.users.all():
                return c.persen
        return 0



def add_order(request,RefID):
        try:
            pay_type = request.session['pay_type']
        
            information_order=request.session['information_order']
            user = None

            if request.user.is_authenticated:
                user=request.user
            order=OrderModel.objects.create(user=user,name=information_order['fulname'],email=information_order['email'],address=information_order['address'],
                                                phone=information_order['phone'],ostan=information_order['ostan'],
                                                city=information_order['city'],codepsty=information_order['codepsty'],
                                                pay_type=pay_type,price_all=Cart(request).get_order_price(),price_with_post=Cart(request).get_order_price_with_post_price(pay_type))
            cart = Cart(request).cart
            for product_id,item in cart.items():
                product = ProductModel.objects.get(id=product_id)
                OrderItemsModel.objects.create(order=order,product=product,price=item['price'],number=item['number'])
                order.ref_id=RefID
                order.paid=True
                order.save()
                request.session['cart']={}
                request.session['information_order']={}
                return True
        except:
            return False
        
class Is_Admin_User_Mixin(UserPassesTestMixin):
    def test_func(self):
        return  self.request.user.is_authenticated and self.request.user.is_admin