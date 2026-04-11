from django.urls import path
from .views import (
    evosView, qirikodView, MalumotView, turarjoyView,
    save_application, ProductDetailView, manzilView, ShoppingCartList,
    add_to_cart, remove_to_cart, UserRegisterView, UserLoginView, savatView,
    chekautView, kartaView, yangilikView, kontaklarView, filyalView, vacaView,
    arizaView, tableView, akvagrimView, uyingohView, sovgaView, 
    dashboard_view, operatorView, order_detailView, orderView, dashboardView
)

urlpatterns = [
    # Asosiy sahifalar
    path('', evosView.as_view(), name='aa'),
    path('qirikod/', qirikodView.as_view(), name='qirikod'),
    path('malumot/', MalumotView.as_view(), name='malumot'),
    path('turarjoy/', turarjoyView.as_view(), name='turarjoy'),
    path('manzil/', manzilView.as_view(), name='manzil'),
    
    # Avtorizatsiya
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    
    # Savatcha va Buyurtma (Cart & Checkout)
    path('shopping-cart/', ShoppingCartList.as_view(), name='shopping_cart'),
    path('savat/', savatView.as_view(), name='savat'),
    path('chekaut/', chekautView.as_view(), name='chekaut'),
    path('add-to-cart/', add_to_cart, name='add_cart'),
    path('remove-to-cart/<int:pk>/', remove_to_cart, name='remove-cart'),
    path('carta/', kartaView.as_view(), name='carta'),
    
    # Mahsulot tafsiloti
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),

    # Dashboard va Operator paneli
    path('dashboard/', dashboard_view, name='dashboard'),
    path('order-dashboard/', dashboardView.as_view(), name='order_dashboard_class'),
    path('operator/', operatorView.as_view(), name='operator_list'),# Bu yerda 'operator_list' views.py bilan moslandi
    path('orders/', orderView.as_view(), name='order_list'),
    path('order/<int:pk>/', order_detailView.as_view(), name='order_detail'),

    # Biz haqimizda va Yangiliklar
    path('yangilik/', yangilikView.as_view(), name='yangilik'),
    path('kontaklar/', kontaklarView.as_view(), name='kontaklar'),
    path('felyal/', filyalView.as_view(), name='felyal'),
    path('vaca/', vacaView.as_view(), name='vaca'),
    path('ariza/', arizaView.as_view(), name='ariza'),
    path('table/', tableView.as_view(), name='table'),

    # Bolalar uchun (Kids)
    path('akvagrim/', akvagrimView.as_view(), name='akvagrim'),
    path('uyingoh/', uyingohView.as_view(), name='uyingoh'),
    path('sovga/', sovgaView.as_view(), name='sovga'),

    # Arizalarni saqlash
    path('turarjoy/ariza/', save_application, name='evos_form'),
    path('turarjoy/save/', save_application, name='save_application'),
]