from multiprocessing import context
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny 
from .models import VerifyType, ProductType, NationType, StoreType, Category, EntryType, FinalType
from users.models import UserVerifyModel, ProfileModel
from content.models import ContentModel, FileModel
from .serializer import VerifyTypeSerializer, ProductTypeSerializer, NationTypeSerializer, StoreTypeSerializer, CategorySerializer, EntryTypeSerializer
from users.serializer import ProfileModelSerializer, UserVerifyModelSerializer
from content.serializer import ContentModelSerializer, FileModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import json, os
from django.core.files.storage import default_storage
import uuid
from django.conf import settings
from django.core.files import File
from pathlib import Path
import json
from io import BytesIO, StringIO
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile

# from django.http import HttpResponse, JsonResponse

# Create your views here.


class EntryTypeView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = EntryTypeSerializer
    queryset = EntryType.objects.all()


class VerifyTypeView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = VerifyTypeSerializer
    queryset = VerifyType.objects.all()


class ProductTypeView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()

    @action(detail=True, methods=['get'], url_path='all-products')
    def re_order( self, request, pk=None):
        temp = self.queryset.filter(product_category_id=pk)
        serializer = ProductTypeSerializer( temp, many=True)
        return Response( serializer.data)

class NationTypeView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = NationTypeSerializer
    queryset = NationType.objects.all()

class StoreTypeView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = StoreTypeSerializer
    queryset = StoreType.objects.all()


class CategoryView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['get'], url_path='cate-gory')
    def get_category( self, request, pk):

        if pk == "0":
            temp = Category.objects.all()
            serializer = CategorySerializer( temp, many=True)
            return Response( serializer.data)
            
        else:
            temp = self.queryset.filter(id=pk)
            serializer = CategorySerializer( temp, many=True)
            return Response( serializer.data)



class FinalizeView( generics.GenericAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # permission_classes = [AllowAny]

    user_queryset = UserVerifyModel.objects.all()
    profile_queryset = ProfileModel.objects.all()
    content_queryset = ContentModel.objects.all()
    file_queryset = FileModel.objects.all()
    product_type_queryset = ProductType.objects.all()



    user_serializer_class = UserVerifyModelSerializer
    profile_serializer_class = ProfileModelSerializer
    content_serializer_class = ContentModelSerializer
    file_serializer_class = FileModelSerializer
    product_type_serializer_class = FileModelSerializer


    def get(self, request, pk):

        try:
            user_model = self.user_queryset.filter(id=pk)[0]
            user_data = self.user_serializer_class( user_model, many=False).data
        except:
            user_model = None
            user_data = None

        try:
            profile_model = self.profile_queryset.filter(user_mail_id=pk)[0]
            profile_data = self.profile_serializer_class( profile_model, many=False).data

        except:
            profile_model = None
            profile_data = None

        try:
            content_model = self.content_queryset.filter(user_mail_id=pk)[0]
            content_data = self.content_serializer_class( content_model, many=False).data
            
            # print ( json.loads( content_data.get("sub_title")))

            # print ( profile_data.get)

            product_type_id = profile_data.get("product_type")
            text_array = json.loads( content_data.get("sub_title"))
            temp_text = []

            ### subtitle to json ###
            if product_type_id != None:
                product_type = self.product_type_queryset.filter(pk = product_type_id)[0]
                text_filter = json.loads( product_type.input_box)
                temp_text = []
                for i in text_array:
                    real_context =(text_filter[i["index"]])
                    all_text = i["text_array"]

                    temp_json = {
                        "index" : i["index"],
                        "text" : []
                    }
                    temp_each_json = {}
                    for j in all_text:
                        if j['index'] in real_context:
                            temp = { 
                            }

                            temp_each_json[j.get("index")] = j.get("text")
                    temp_json["text"] = temp_each_json
                    temp_text.append( temp_json)
            content_data["sub_title"] = temp_text


            for i in range( 0, 15):
                ids = content_data.get("photo_" + str( i))
                json_files = self.file_queryset.filter( id__in=ids).order_by('order')
                files = self.file_serializer_class( json_files, many=True)
                content_data["photo_" + str(i)] = files.data
        except:
            content_model = None
            content_data = None

        json_return = []

        for i in [user_data, profile_data, content_data]:
            json_return.append( i)

        


        file = 'student_file.json'
        # with open(file, "w") as json_file:
        #     json.dump(json_return, json_file)

        aaaaa = ContentFile( file, b"asdf")
        
        aaaa = default_storage.save("invoice/", file)


        final_mod = FinalType(file_end = aaaa)
        final_mod.save()
        # aaaa = default_storage.save("invoice/", file)


        # json_file.seek(0)


        # unique_filename = os.path.join( "invoice/" + str(uuid.uuid4()) + ".json")


        # with open(unique_filename, 'w') as outfile:
        #     json.dump(json_return, unique_filename)

        # filename = 'aaaa.txt'
        # path = "invoice/"

        # f = 'invoice/aaaa.txt'
        # print (f)
        # my_file = File(f)


        # aaaa = default_storage.save("invoice/", f)
        # version = FinalType(end_file = aaaa)
        # version.save()



        #file = ContentFile(  "ASdfsadf")
        #aaaa = default_storage.save("invoice/test.json", file)
        # fs = FileSystemStorage(location="invoice/") 
        # filename  = fs.save(outfile.name, outfile)
        # file_url = fs.url(filename)
        # print ( file_url)

        return Response(json_return)  
