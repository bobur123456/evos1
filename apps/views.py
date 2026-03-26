from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Qirikod,Application, Product


class evosView(TemplateView):
    template_name = "base.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.all()
        return context
    
    
    
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