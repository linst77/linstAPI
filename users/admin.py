from django.contrib import admin
from .models import ProfileModel, UserVerifyModel

# Register your models here.
@admin.register( UserVerifyModel)
class FileAdmin( admin.ModelAdmin):
    list_display = ['id', 'user_mail', 'nation', 'store', 'product_category', 'product_type']

@admin.register( ProfileModel)
class FileAdmin( admin.ModelAdmin):
    list_display = ['id', 'user_mail', 'nation', 'store', 'product_category', 'product_type']