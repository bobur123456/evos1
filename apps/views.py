from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Qirikod,Application, Product,Category, ShoppingCart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from django.contrib.auth import login, logout
from apps.forms import UserLoginForm, UserRegisterForm
from apps.mixsins import NotLoginRequiredMixin
from .models import Users
from django.views.generic import TemplateView
from .models import (
    Users, 
    Qirikod, 
    Application, 
    Product, 
    Category, 
    ShoppingCart, 
    Order, 
    OrderItem, 
    Coupon
)

from django.views.generic import TemplateView,CreateView, FormView


class evosView(ListView):
    model = Category
    template_name = "base.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.all()
        context['category'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        
        category = self.request.GET.get('category')
        
        if category:
            
            return Product.objects.filter(category__name=category).first()
        
        return Product.objects.all()
    
class manzilView(TemplateView):
    template_name = "product/manzil.html"
        
    
    
    
class qirikodView(TemplateView):
    template_name = "product/evos.html"
    
    

class MalumotView(ListView):
    model = Qirikod
    template_name = "product/hamkorlar.html"
    context_object_name = "products"
    
    
    

class turarjoyView(TemplateView):    
    template_name = "product/turar_joy.html"
   



def save_application(request):
    if request.method == 'POST':
        person_type = request.POST.get('person_type')
        full_name = request.POST.get('full_name')
        inn = request.POST.get('inn')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        area = request.POST.get('area')
        files = request.FILES.get('files') # Rasm yoki fayl

        # Bazaga saqlash
        Application.objects.create(
            person_type=person_type,
            full_name=full_name,
            inn=inn,
            email=email,
            phone=phone,
            area=area,
            file=files
        )
        return render(request, 'success.html') 
    
    return render(request, 'evos_form.html')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    slug_field = "slug"
    




class savatView(TemplateView):
    template_name = 'product/savat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Savatdagi mahsulotlar (Sessiyadan olish o'rniga hozircha bazadan test uchun)
        products = Product.objects.filter(is_active=True)[:2] 
        
        cart_items = []
        total_price = 0
        
        for prod in products:
            quantity = 1 
            
            # Agar modelingizda sale (chegirma) bo'lsa, narxni hisoblaymiz
            current_price = prod.price
            if prod.sale > 0:
                current_price = prod.price * (100 - prod.sale) / 100
                
            item_total = current_price * quantity
            total_price += item_total
            
            cart_items.append({
                'product': prod,
                'quantity': quantity,
                'subtotal': int(item_total)  # HTMLdagi subtotal bilan mos kelishi uchun
            })
            
        context['cart_items'] = cart_items
        context['total_price'] = int(total_price)
        return context





@login_required(login_url='login')
def add_to_cart(request):
    
    if request.method == "POST":
        data = request.POST
        product_id = data.get('product')
        user_id = request.user.id
        new_cart = ShoppingCart.objects.create(
            product_id=product_id,
            user_id=user_id
        )
        new_cart.save()
        
        return redirect('shopping_cart')


@login_required(login_url='login')
def remove_to_cart(request, pk):
    product_id = pk
    user_id = request.user.id
    db_card = ShoppingCart.objects.filter(id=product_id, user_id=user_id)
    if db_card.exists():
        db_card.delete()
        return redirect('shopping_cart')
    return redirect('shopping_cart')




class UserRegisterView(NotLoginRequiredMixin, CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'auth/register.html'
    success_url = '/'



class UserLoginView(NotLoginRequiredMixin, FormView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        db_user = Users.objects.filter(username=username).first()
        
        if db_user and db_user.check_password(password):
            if db_user.user_type == "operator":
                messages.success(self.request, "Xush kelibsiz ✅")
                login(self.request, db_user)
                return redirect('operator_list')
            else:
                login(self.request, db_user)
                messages.success(self.request, "Xush kelibsiz ✅")
                return redirect(self.success_url)
        
        messages.error(self.request, "Parol yoki Login Xato ❌")
        return self.form_invalid(form)
    




class ShoppingCartList(LoginRequiredMixin, TemplateView):
    template_name = 'product/shopping-cart.html'
    login_url = 'login'


@login_required(login_url='login')
def add_to_cart(request):
    
    if request.method == "POST":
        data = request.POST
        product_id = data.get('product')
        user_id = request.user.id
        new_cart = ShoppingCart.objects.create(
            product_id=product_id,
            user_id=user_id
        )
        new_cart.save()
        
        return redirect('shopping_cart')


@login_required(login_url='login')
def remove_to_cart(request, pk):
    product_id = pk
    user_id = request.user.id
    db_card = ShoppingCart.objects.filter(id=product_id, user_id=user_id)
    if db_card.exists():
        db_card.delete()
        return redirect('shopping_cart')
    return redirect('shopping_cart')
class chekautView(TemplateView):
    template_name = 'product/chekaut.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Savatni sessiyadan olish
        cart = self.request.session.get('cart', {})
        
        total_price = 0
        total_asl_price = 0
        items_list = []

        # 2. Savatdagi har bir mahsulotni aylana bo'ylab hisoblash
        for product_id, item_data in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                quantity = int(item_data.get('quantity', 1))
                
                # Mahsulotning asl narxi (chegirmasiz)
                total_asl_price += product.price * quantity
                
                # Mahsulotning sotuv narxi (agar sale bo'lsa o'shani oladi, bo'lmasa asosiy narx)
                # Agar mahsulotda sale foiz bo'lsa: yakuniy_narx = price - (price * sale / 100)
                if product.sale and product.sale > 0:
                    current_item_price = product.price * (1 - product.sale / 100)
                else:
                    current_item_price = product.price
                
                total_price += current_item_price * quantity
                
                items_list.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': current_item_price * quantity
                })
            except Product.DoesNotExist:
                continue

        # 3. Savatchada qo'llanilgan umumiy promokodni tekshirish (10% kabi)
        promo_discount = self.request.session.get('promo_discount', 0)
        if promo_discount > 0:
            total_price = total_price * (1 - promo_discount / 100)

        # 4. HTMLga ma'lumotlarni yuborish
        context['items'] = items_list
        context['asl_narxi'] = int(total_asl_price)
        context['jami_narx'] = int(total_price)
        context['chegirma_foizi'] = promo_discount
        
        # Eski koddagi bitta mahsulotni ham yuborib turamiz (xatolik bermasligi uchun)
        if items_list:
            context['product'] = items_list[0]['product']
        
        return context

        
class kartaView(TemplateView):
    template_name = 'product/carta.html'



class yangilikView(TemplateView):
    template_name = 'bizhaqimizda/yangiliklar.html'


class kontaklarView(TemplateView):
    template_name = 'bizhaqimizda/kontaklar.html'


class filyalView(TemplateView):
    template_name = 'bizhaqimizda/filyalar.html'




class vacaView(TemplateView):
    template_name = 'bizhaqimizda/vacancy.html'


class arizaView(TemplateView):
    template_name = 'bizhaqimizda/ariz_topshirish.html'




class tableView(TemplateView):
    template_name = 'bizhaqimizda/table.html'



class akvagrimView(TemplateView):
    template_name = 'kids/akvagrim.html'



class uyingohView(TemplateView):
    template_name = 'kids/maydoncha.html'



class sovgaView(TemplateView):
    template_name = 'kids/bayram.html'


class ShoppingCartList(LoginRequiredMixin, TemplateView):
    template_name = 'product/shopping-cart.html'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        """Promokodni qabul qilish qismi"""
        promo_code = request.POST.get('promo_code')
        if promo_code:
            try:
                # Kodni bazadan tekshirish
                coupon = Coupon.objects.get(code__iexact=promo_code, active=True)
                
                # Vaqtini va limitini tekshirish
                if coupon.valid_to >= timezone.now() and coupon.used_count < coupon.usage_limit:
                    request.session['discount_percent'] = coupon.discount_percent
                    messages.success(request, f"{coupon.discount_percent}% chegirma qo'llanildi!")
                else:
                    messages.error(request, "Bu promokod muddati tugagan.")
                    request.session['discount_percent'] = 0
            except Coupon.DoesNotExist:
                messages.error(request, "Bunday promokod mavjud emas.")
                request.session['discount_percent'] = 0
        
        return redirect('shopping_cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Savatchadagi mahsulotlar
        cart_items = ShoppingCart.objects.filter(user=user)
        
        # Jami narxni hisoblash
        total_price = sum(item.product.price for item in cart_items)
        
        # Sessiyadan chegirma foizini olish
        discount_percent = self.request.session.get('discount_percent', 0)
        
        # Chegirma miqdori va yakuniy narx
        discount_amount = (total_price * discount_percent) / 100
        final_price = total_price - discount_amount

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        context['final_price'] = final_price
        context['discount_percent'] = discount_percent
        return context


# Operatorlar uchun View (Class-based)
class operatorView(LoginRequiredMixin, TemplateView):
    template_name = 'order/operator.html'
    login_url = 'login'  # Agar login qilmagan bo'lsa, qayerga yuborishni ko'rsatish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all().order_by('-created_at')
        
        context['order_list'] = orders
        context['total_count'] = orders.count()
        context['new_count'] = orders.filter(is_status='pending').count()
        
        # Xatolik chiqmasligi uchun hasattr bilan tekshiramiz
        total = 0
        for order in orders:
            if hasattr(order, 'total_order_price'):
                # Agar funksiya bo'lsa (), bo'lmasa o'zini qo'shamiz
                val = order.total_order_price() if callable(order.total_order_price) else order.total_order_price
                total += val or 0
        
        context['total_revenue'] = total
        return context
# Umumiy Dashboard (Function-based)
@login_required
def dashboard_view(request):
    # Foydalanuvchi turiga qarab filtrlash
    user_type = getattr(request.user, 'user_type', 'customer')
    
    if user_type in ['admin', 'operator']:
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Mijoz faqat o'zinikini ko'radi
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Statistika (Optimallashtirilgan variant)
    total_orders = orders.count()
    new_orders = orders.filter(is_status='pending').count()
    total_revenue = sum(order.total_order_price for order in orders)

    context = {
        'order_list': orders,
        'total_count': total_orders,
        'new_count': new_orders,
        'total_revenue': total_revenue,
    }
    
    # Sizning operatorView klassingizda 'order/dashboard.html' deb ko'rsatilgan
    # Shuning uchun bu yerda ham yo'lni to'g'rilab qo'yamiz:
    return render(request, 'order/dashboard.html', context)

class order_detailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html' # O'zingizning shabloningiz nomi
    context_object_name = 'order'



class orderView(TemplateView):
    template_name = 'order/order.html'



class dashboardView(TemplateView):
    template_name = 'order/dashboard.html'
