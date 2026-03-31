from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import Qirikod,Application, Product,Category, ShoppingCart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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