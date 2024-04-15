from django.contrib import admin
from .models import User, Category, Course, Instructor, Area, Client, Comment, Cart, CartItem, Purchase

# Register your models here.
class PurchaseAdmin(admin.ModelAdmin):
    filter_horizontal = ("courses",)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Area)
admin.site.register(Client)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Purchase, PurchaseAdmin)