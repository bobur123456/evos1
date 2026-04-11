from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Category, Product, Tags, ProductImage, 
    Application, Qirikod, Banner, Coupon, ShoppingCart,
    Users, Order, OrderItem, ManzilSaqlash
)

# 1. Oddiy modellarni ro'yxatdan o'tkazish
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(ProductImage)
admin.site.register(Application)
admin.site.register(Qirikod)
admin.site.register(Banner)
admin.site.register(ManzilSaqlash)

# 2. Foydalanuvchilar (Users) admini
@admin.register(Users)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('user_type', 'avatar', 'banner', 'intro')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('user_type',)}),
    )

# 3. Mahsulotlar (Product) admini
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_active', 'is_hit']
    list_editable = ['price', 'is_active', 'is_hit']
    search_fields = ['name']

# 4. Promokodlar (Coupon) admini
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_to', 'active', 'used_count']
    list_filter = ['active', 'valid_to']
    search_fields = ['code']
    list_editable = ['active']

# 5. Savatcha (ShoppingCart) admini
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['user', 'created_at']

# 6. Buyurtmalar (Order) va ularning ichidagi mahsulotlar (OrderItem)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Bo'sh qatorlar chiqmasligi uchun
    readonly_fields = ['product_name', 'price', 'quantity'] # Operator o'zgartira olmasligi uchun

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'is_status', 'payment_method', 'created_at')
    list_filter = ('is_status', 'payment_method', 'created_at')
    search_fields = ('id', 'phone', 'user__username')
    list_editable = ('is_status',) # Statusni ro'yxatning o'zida o'zgartirish
    inlines = [OrderItemInline]