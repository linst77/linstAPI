from django.db import models
import os
import string, random
from django.utils.text import slugify


# Create your models here.
class EntryType( models.Model):
    url_no_create = models.BooleanField( default=False)
    login_no_create = models.BooleanField( default=False)
    url_popup = models.BooleanField( default=True)
    login_popup = models.BooleanField( default=True)

    def __str__( self):
        return str( self.id)


class VerifyType( models.Model):
    email_verify = models.BooleanField( default=True)
    phone_verify = models.BooleanField( default=False)

    def __str__( self):
        return str( self.id)


class Category( models.Model):
    category = models.CharField( max_length=200, null=True, blank=True)
    def __str__( self):
        return str( self.category)


def storeimage_path(instance, filename):
    # return os.path.join(f'images/{filename}')
    return os.path.join(f'images/temp/store/{instance.id}/{filename}')

class StoreType( models.Model):
    store_title = models.CharField( max_length=200, null=True, blank=True)
    store_intro = models.CharField( max_length=200, null=True, blank=True)
    file_01 = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    file_02 = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    file_03 = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    file_04 = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    file_05 = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    file_login = models.ImageField( upload_to=storeimage_path, null=True, blank=True)
    store_phone = models.CharField( max_length=200, null=True, blank=True)
    store_address = models.CharField( max_length=200, null=True, blank=True)
    slug = models.SlugField(db_index=True, unique=True, max_length=200, blank=True, null=True)

    def __str__( self):
        return self.store_title

    def save(self, *args, **kwargs):
        slug_suffix = []
        for i in range(6):
            slug_suffix.append( random.choice(string.ascii_letters))
        slug = slugify(str( self.store_title) + "-"+ ''.join(slug_suffix), allow_unicode=True)
        self.slug = slug
        super(StoreType, self).save(*args, **kwargs)

def nationimage_path(instance, filename):
    return os.path.join(f'images/temp/nation/{instance.id}/{filename}')

class NationType( models.Model):
    nation_title = models.CharField( max_length=200, null=True, blank=True)
    files = models.ImageField( upload_to=nationimage_path, null=True, blank=True)
    nation_phone = models.CharField( max_length=200, null=True, blank=True)
    nation_address = models.CharField( max_length=200, null=True, blank=True)
    slug = models.SlugField(db_index=True, unique=True, max_length=200, blank=True, null=True)

    def __str__( self):
        return self.nation_title

    def save(self, *args, **kwargs):
        slug_suffix = []
        for i in range(6):
            slug_suffix.append( random.choice(string.ascii_letters))
        slug = slugify(str( self.nation_title) + "-"+ ''.join(slug_suffix), allow_unicode=True)
        self.slug = slug
        super(NationType, self).save(*args, **kwargs)


class ProductType( models.Model):
    product_category = models.ForeignKey( Category, on_delete=models.CASCADE, blank=True, null=True, related_name="product_category")
    product_type = models.CharField( max_length=200, blank=True, null=True)
    items = models.IntegerField(blank=True, null=True)
    counts = models.CharField( max_length=200, blank=True, null=True)
    input_box = models.CharField( max_length=200, blank=True, null=True)
    description_index = models.CharField( max_length=300, blank=True, null=True)

    content_text = models.CharField( max_length=200, blank=True, null=True)
    guide_text = models.CharField( max_length=200, blank=True, null=True)
    image_url = models.URLField(  max_length=200, blank=True, null=True)
    review_url = models.URLField(  max_length=200, blank=True, null=True)
    parts = models.CharField( max_length=500, null=True, blank=True)
    def __str__( self):
        return self.product_type + ": " + str( self.id)