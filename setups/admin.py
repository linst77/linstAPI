from django.contrib import admin
from .models import ProductType, VerifyType, StoreType, NationType, Category, EntryType
# Register your models here.

@admin.register( EntryType)
class EntryTypeAdmin( admin.ModelAdmin):
    list_display = ['url_no_create', 'login_no_create', 'url_popup', 'login_popup']

@admin.register( VerifyType)
class VerifyTypeAdmin( admin.ModelAdmin):
    list_display = ['id', 'email_verify', 'phone_verify']

@admin.register( ProductType)
class ProductTypeAdmin( admin.ModelAdmin):
    list_display = ['id', 'product_category', 'product_type', 'counts']

@admin.register( StoreType)
class StoreTypeAdmin( admin.ModelAdmin):
    list_display = ['id', 'store_title', 'store_phone']

@admin.register( NationType)
class NationTypeAdmin( admin.ModelAdmin):
    list_display = ['id', 'nation_title', 'nation_phone']

@admin.register( Category)
class CategoryAdmin( admin.ModelAdmin):
    list_display = ['id', 'category']