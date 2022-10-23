from django.db import models
from setups.models import ProductType, Category, NationType, StoreType
from django.utils.text import slugify
import string, random
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


# Create your models here.

class UserVerifyModel( models.Model):
    ### This is login ###
    user_mail = models.EmailField( max_length=254, blank=True, null=True)
    user_phone = models.IntegerField( blank=True, null=True)
    
    ### Extra information ###
    order_name = models.CharField( max_length=200, blank=True, null=True)
    nation = models.IntegerField( blank=True, null=True)
    store = models.IntegerField( blank=True, null=True)
    product_category = models.IntegerField( blank=True, null=True)
    product_type = models.IntegerField( blank=True, null=True)
    process_step = models.IntegerField( default=0, blank=True, null=True)

    # product_type = models.ForeignKey( ProductType, on_delete=models.CASCADE, blank=True, null=True)
    option = models.CharField( max_length=100, blank=True, null=True)
    slug = models.SlugField(db_index=True, unique=True, max_length=200, blank=True, null=True)

    def __str__( self):
        return str( self.user_mail)

    def save(self, *args, **kwargs):
        slug_suffix = []
        for i in range(30):
            slug_suffix.append( random.choice(string.ascii_letters))
        slug = slugify(str( self.user_mail) + ''.join(slug_suffix), allow_unicode=True)
        self.slug = slug
        super(UserVerifyModel, self).save(*args, **kwargs)

class ProfileModel( models.Model):
    ### Login info ###
    user_mail = models.ForeignKey( UserVerifyModel, on_delete=models.CASCADE, related_name="user_mail_sel")    
    user_phone = models.IntegerField( blank=True, null=True)
    # pre_product_type = models.ForeignKey( ProductType, on_delete=models.CASCADE, blank=True, null=True)

    ### User Information
    order_name = models.CharField( max_length=200, blank=True, null=True)
    name_a = models.CharField( max_length=200, blank=True, null=True)
    name_b = models.CharField( max_length=200, blank=True, null=True)
    name_c = models.CharField( max_length=200, blank=True, null=True)
    location = models.CharField( max_length=200, blank=True, null=True)
    event_date = models.CharField( max_length=200, blank=True, null=True)

    ### nation & store
    nation = models.ForeignKey( NationType, on_delete=models.CASCADE, blank=True, null=True, related_name="nation_type_sel")
    store = models.ForeignKey( StoreType, on_delete=models.CASCADE, blank=True, null=True, related_name="store_type_sel")

    ### product type
    product_type = models.ForeignKey( ProductType, on_delete=models.CASCADE, blank=True, null=True, related_name="product_type_sel")
    product_category = models.ForeignKey( Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category_sel")


    ### process steps
    process_step = models.IntegerField( default=0, blank=True, null=True) 
    preview = models.URLField(  max_length=200, blank=True, null=True)
    finalview = models.URLField( max_length=200, blank=True, null=True)

    ## extra
    extra_info = models.TextField(blank=True, null=True)
    slug = models.SlugField( db_index=True, allow_unicode=True, blank=True, null=True)    

    def __str__( self):
        return str( self.user_mail)

    def save(self, *args, **kwargs):
        if self.product_type != None:
            self.pre_product_type = self.product_type

        super(ProfileModel, self).save(*args, **kwargs)

    @receiver(post_save, sender=UserVerifyModel)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            product_t = []
            product_c = []
            product_n = []
            product_s = []
            step = 1
            try:
                product_t = ProductType.objects.get( pk = instance.product_type)
            except:
                product_t = None
            try:
                product_c = Category.objects.get( pk = instance.product_category)
            except:
                product_c = None
            try:
                product_n = NationType.objects.get( nation_phone = instance.nation)
            except:
                product_n = None
            try:
                product_s = StoreType.objects.get( pk = instance.store)
            except:
                product_s = None

            if product_c != None:
                step = 2
            if product_t != None:
                step = 3

            ProfileModel.objects.create(
                                    user_mail=instance,
                                    user_phone = instance.user_phone,
                                    order_name = instance.order_name,
                                    nation = product_n,
                                    store = product_s,
                                    product_category = product_c,
                                    product_type = product_t,
                                    process_step = step,
                                    slug = instance.slug,
                                    )
