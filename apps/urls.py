from django.urls import path
# Bu yerga save_application funksiyasini ham qo'shib qo'yamiz
from .views import evosView, qirikodView, MalumotView, turarjoyView, save_application, ProductDetailView,manzilView, ShoppingCartList, add_to_cart, remove_to_cart

urlpatterns = [
    path('', evosView.as_view(), name='aa'),
    path('qirikod/', qirikodView.as_view(), name='qirikod'),
    path('malumot/', MalumotView.as_view(), name='malumot'),
    path('turarjoy/', turarjoyView.as_view(), name='turarjoy'),
    path('manzil/', manzilView.as_view(), name='manzil'),
    path('savat/', ShoppingCartList.as_view(), name='savat'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    
    # Formani ko'rsatish va saqlash manzillari
    path('turarjoy/ariza/', save_application, name='evos_form'),
    path('turarjoy/save/', save_application, name='save_application'),
    path('add-to-card/', add_to_cart, name='add_cart'),
    path('remove-to-cart', remove_to_cart, name='remove-cart'),
    
    
]