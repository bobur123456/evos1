from django.urls import path
# Bu yerga save_application funksiyasini ham qo'shib qo'yamiz
from .views import evosView, qirikodView, MalumotView, turarjoyView, save_application, ProductDetailView

urlpatterns = [
    path('', evosView.as_view(), name='aa'),
    path('qirikod/', qirikodView.as_view(), name='qirikod'),
    path('malumot/', MalumotView.as_view(), name='malumot'),
    path('turarjoy/', turarjoyView.as_view(), name='turarjoy'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    
    # Formani ko'rsatish va saqlash manzillari
    path('turarjoy/ariza/', save_application, name='evos_form'),
    path('turarjoy/save/', save_application, name='save_application'),
]