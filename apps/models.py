import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from datetime import datetime, timedelta, timezone

class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Users(AbstractUser):

    class UserTypeChoice(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENT = 'client', 'Mijoz'
        OPERATOR = 'operator', 'Operator'

    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    banner = models.ImageField(upload_to='banner/', blank=True, null=True)
    intro = models.CharField(max_length=500, blank=True, null=True)
    user_type = models.CharField(
        max_length=30,
        choices=UserTypeChoice.choices,
        default=UserTypeChoice.CLIENT
    )

    def __str__(self):
        return self.username
    

    @property
    def full_name(self):
        return f"{self.first_name} - {self.last_name}"
    
    

class Category(BaseCreatedModel):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name

class Tags(BaseCreatedModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    


class Product(BaseCreatedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=300, unique=True, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Narxi")
    sale = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], default=0)
    description = models.TextField(verbose_name="Tarkibi/Haqida")
    count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_hit = models.BooleanField(default=False, verbose_name="Sotuv xitimi?")
    tags = models.ManyToManyField(Tags, blank=True, related_name='tag_list')

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.name)
            while Product.objects.filter(slug=self.slug).exists():
                slugger = str(uuid.uuid4()).split('-')[-1]
                self.slug = f"{slugify(self.name)}-{slugger}"
        super().save(*args, **kwargs)

    @property
    def is_new(self):
        now = datetime.now(timezone.utc)
        return (now - self.created_at) < timedelta(days=2)

    def __str__(self):
        return self.name
    
    


# 5. Qo'shimcha rasmlar (agar kerak bo'lsa)
class ProductImage(BaseCreatedModel):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='img')

# 6. QR Kod tizimi
class Qirikod(BaseCreatedModel):
    name = models.CharField(max_length=100, verbose_name="QR kod nomi")
    link = models.URLField()

    def __str__(self):
        return self.name

# 7. Arizalar (Foydalanuvchilar yuborgan)
class Application(BaseCreatedModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.full_name

# 8. Banner (Aksiya rasmlari uchun)
class Banner(BaseCreatedModel):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    subtitle = models.TextField(verbose_name="Kichik matn")
    image = models.ImageField(upload_to='banners/', verbose_name="Banner rasmi")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    
class ManzilSaqlash(BaseCreatedModel):
    manzil = models.CharField(max_length=255, verbose_name="Manzil nomi")
    uy = models.CharField(max_length=50, blank=True, null=True, verbose_name="Uy/Ofis")
    domofon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Domofon")
    kirish = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kirish")
    qavat = models.CharField(max_length=50, blank=True, null=True, verbose_name="Qavat")
    izoh = models.TextField(blank=True, null=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True) # Qachon saqlanganini bilish uchun

    def __str__(self):
        return f"{self.manzil} - {self.uy}-uy"
    

class ShoppingCart(BaseCreatedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_list')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='my_carts')
    
    def __str__(self):
        return self.user.username