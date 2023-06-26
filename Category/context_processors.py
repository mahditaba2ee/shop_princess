from .models import CategoryModel
from Orders.cart import Cart
from utils.utils import shopping_cart
def category(request):
    all_like_me_count=0
    buys = []
    if request.session.get('cart') is not None:
            # ایدی محصولاتی که در سبد خرید موجود است را نمایش میدهد 
            buys = shopping_cart(request)
        
    if request.user.is_authenticated:
        all_like_me_count = request.user.all_like_me_count()
    cart = Cart(request)
    return {'categories':CategoryModel.objects.all(),'all_like_me_count':all_like_me_count,'len_cart':cart.get_len_cart,'cart':cart,'buys':buys}