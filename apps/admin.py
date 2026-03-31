from django.contrib import admin
from .models import Category, Product, Tags, ProductImage, Application, Qirikod,Category,  Banner


# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(ProductImage)
admin.site.register(Application)
admin.site.register(Qirikod)
admin.site.register(Banner)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'id']
    






