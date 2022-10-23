from django.db.models.signals import post_save
from django.dispatch import receiver
from setups.models import ProductType
from users.models import ProfileModel, UserVerifyModel
from .models import ContentModel, FileModel
import json

@receiver(post_save, sender=ProfileModel)
def update_model(sender, instance, created, **kwargs):

    if created == False:
        user_account = UserVerifyModel.objects.get(pk=instance.user_mail_id)
        
        if instance.product_type_id is None:
            delete_item = FileModel.objects.filter( user_mail_id = instance.user_mail_id)
            if delete_item:
                delete_item.delete()

        if instance.product_type_id is not None:
            # Update User account

            if user_account.product_type != instance.product_type_id:
                delete_item = FileModel.objects.filter( user_mail_id = instance.user_mail_id)
                if delete_item:
                    delete_item.delete()

            elif user_account.product_type == instance.product_type_id:
                return
                
            user_account.product_type = instance.product_type_id
            user_account.save()
            # Update Content page
            product_page = ContentModel.objects.get(slug=instance.slug)
            product_page.product_type_id = instance.product_type_id
            # product_page.save()
            #fild files

            count = FileModel.objects.filter(user_mail_id = instance.user_mail_id)
            if len( count) == 0:
                product_type = ProductType.objects.get( id = instance.product_type_id)
                all_items = product_type.items
                all_count = json.loads(product_type.counts)

                data = []
                for x in range( all_items):
                    index_data = {
                        "index" : x,
                        "text_array" :[]
                    }
                    for y in range( all_count[x]):
                        sub_data = {
                            "index" : y,
                            "text" : ""
                        }
                        index_data["text_array"].append( sub_data)
                    data.append( index_data)
                    product_page.sub_title = json.dumps( data)
                    product_page.save()

                for i in range(all_items):
                    file_group = []
                    for j in range( all_count[i]):
                        file_group.append( FileModel(   
                                                        files = "images/temp/image_sample.jpg",
                                                        thumbnail = "images/temp/thumb_sample.jpg",
                                                        user_mail_id = instance.user_mail_id,
                                                        product_type_id = instance.product_type_id,
                                                        items = i,
                                                        order = j,
                                                        counts = j,
                                                        # slug = instance.slug
                                                    ))
                    ppp = FileModel.objects.bulk_create( file_group)
                    test = eval( "product_page.photo_{}".format(i))
                    test.add( *ppp)

@receiver(post_save, sender=ContentModel)
def update_content_model(sender, instance, created, **kwargs):
    if created:
        print ("Content DB created")
        user_account = UserVerifyModel.objects.get(pk=instance.user_mail_id)
        profile_page = ProfileModel.objects.get(user_mail_id = instance.user_mail_id)



        if profile_page.product_type_id is None:
            delete_item = FileModel.objects.filter( user_mail_id = instance.user_mail_id)
            if delete_item:
                delete_item.delete()
        elif profile_page.product_type_id is not None:

            # Update Content page
            product_page = instance

            #fild files
            count = FileModel.objects.filter(user_mail_id = profile_page.user_mail_id)
            if len( count) == 0:
                product_type = ProductType.objects.get( id = profile_page.product_type_id)
                all_items = product_type.items
                all_count = json.loads(product_type.counts)

                data = []
                for x in range( all_items):
                    index_data = {
                        "index" : x,
                        "text_array" :[]
                    }
                    for y in range( all_count[x]):
                        sub_data = {
                            "index" : y,
                            "text" : ""
                        }
                        index_data["text_array"].append( sub_data)
                    data.append( index_data)
                    product_page.sub_title = json.dumps( data)
                    product_page.save()

                for i in range(all_items):
                    file_group = []
                    for j in range( all_count[i]):
                        file_group.append( FileModel(   
                                                        files = "images/temp/image_sample.jpg",
                                                        thumbnail = "images/temp/thumb_sample.jpg",
                                                        user_mail_id = profile_page.user_mail_id,
                                                        product_type_id = profile_page.product_type_id,
                                                        items = i,
                                                        order = j,
                                                        counts = j,
                                                        slug = profile_page.slug
                                                    ))
                    ppp = FileModel.objects.bulk_create( file_group)
                    test = eval( "product_page.photo_{}".format(i))
                    test.add( *ppp)

