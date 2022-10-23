from django.db import models
from setups.models import ProductType
from users.models import UserVerifyModel, ProfileModel
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
from PIL import Image
from django.core.files import File
from .image_detact import de_alpha, de_thumb

# Create your models here.
def file_path(instance, filename):
    return os.path.join(f'images/{instance.user_mail_id}/{filename}')

def thumb_file_path(instance, filename):
    return os.path.join(f'images/{instance.user_mail_id}/thumb/thum_{filename}')

# Create your models here.
class FileModel( models.Model):
    user_mail = models.ForeignKey( UserVerifyModel, on_delete=models.CASCADE, related_name='file_user', blank=True, null=True)
    product_type = models.ForeignKey( ProductType, on_delete=models.PROTECT, related_name='file_product_type', blank=True, null=True)
    files = models.FileField( upload_to=file_path, null=True, blank=True)
    thumbnail = models.ImageField( upload_to=thumb_file_path, null=True, blank=True)
    items = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    counts = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField( auto_now_add=True)
    slug = models.SlugField( db_index=True, allow_unicode=True, blank=True, null=True)

    def __str__(self):
        return "{}-{}".format( self.user_mail, self.product_type)

    def save(self, *args, **kwargs):
        size_wh = (200, 112)
        # Original Image
        if not self.files:
            return None
        else:
            self.files = de_alpha( self.files)
            self.thumbnail = de_thumb( self.files)

        super(FileModel, self).save(*args, **kwargs)

class ContentModel( models.Model):
    user_mail = models.ForeignKey( UserVerifyModel, on_delete=models.CASCADE, related_name='content_user', blank=True, null=True)
    user_phone = models.IntegerField( blank=True, null=True)
    product_type = models.ForeignKey( ProductType, on_delete=models.PROTECT, related_name='content_type', blank=True, null=True)

    photo_0 = models.ManyToManyField( FileModel, related_name="item_01", blank=True)
    photo_1 = models.ManyToManyField( FileModel, related_name="item_02",  blank=True)
    photo_2 = models.ManyToManyField( FileModel, related_name="item_03",  blank=True)
    photo_3 = models.ManyToManyField( FileModel, related_name="item_04",  blank=True)
    photo_4 = models.ManyToManyField( FileModel, related_name="item_05",  blank=True)
    photo_5 = models.ManyToManyField( FileModel, related_name="item_06",   blank=True)
    photo_6 = models.ManyToManyField( FileModel, related_name="item_07",   blank=True)
    photo_7 = models.ManyToManyField( FileModel, related_name="item_08",  blank=True)
    photo_8 = models.ManyToManyField( FileModel, related_name="item_09",  blank=True)
    photo_9 = models.ManyToManyField( FileModel, related_name="item_10",   blank=True)
    photo_10 = models.ManyToManyField( FileModel, related_name="item_11",   blank=True)
    photo_11 = models.ManyToManyField( FileModel, related_name="item_12",   blank=True)
    photo_12 = models.ManyToManyField( FileModel, related_name="item_13",  blank=True)
    photo_13 = models.ManyToManyField( FileModel, related_name="item_14",   blank=True)
    photo_14 = models.ManyToManyField( FileModel, related_name="item_15",  blank=True)
    sub_title = models.TextField( blank=True, null=True)
    option = models.TextField( max_length=200, blank=True, null=True)
    slug = models.SlugField( db_index=True, allow_unicode=True, blank=True, null=True)

    created = models.DateTimeField( auto_now_add=True)
    updated = models.DateTimeField( auto_now=True)

    class Meta():
        ordering = ['-created', '-user_mail']

    def __str__(self):
        return str( self.user_mail)

    @receiver(post_save, sender=ProfileModel)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            product_type = None
            if instance.product_type_id != None:
                product_type = ProductType.objects.get( id = instance.product_type_id)

            ContentModel.objects.create( user_mail=UserVerifyModel.objects.get(id = instance.user_mail_id),
                                    product_type = product_type,
                                    user_phone = instance.user_phone,
                                    slug=instance.slug
                                    )
