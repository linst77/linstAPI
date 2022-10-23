from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import FileModel, ContentModel
from users.models import ProfileModel
from setups.models import ProductType
from .serializer import FileModelSerializer, ContentModelSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse


# Create your views here.
class FileModelView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FileModelSerializer
    queryset = FileModel.objects.all()

    @action(detail=False, methods=['PATCH'], url_path='cur-fileorder')
    def re_order( self, request):
        
        update = []
        for i in request.data:
            temp = self.queryset.get(id=i["id"])
            temp.order = i.get('order')
            update.append( temp)
        FileModel.objects.bulk_update( update, ['order'])
        return JsonResponse({"Works":"test"})

# Create your views here.
class ContentModelView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ContentModelSerializer
    queryset = ContentModel.objects.all()

    @action(detail=True, methods=['PATCH'], url_path='cur-content')
    def patch_content( self, request, pk=None):
        temp = ContentModel.objects.get(id=pk)
        temp.sub_title = request.data.get("sub_title")
        patch_update = [temp]
        ContentModel.objects.bulk_update( patch_update, ['sub_title'])
        return JsonResponse({"Works":"test"})

    @action(detail=True, methods=['GET'], url_path='cur-context')
    def user_data( self, request, pk):

        user_queryset = self.queryset.filter(user_mail_id=pk)

        if len( user_queryset) > 0:
            temp_user = user_queryset[0]
            serializer = ContentModelSerializer( temp_user, many=False)
            return Response( serializer.data)



# pk = user, pk2 = product type
class FileUserListView( generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = FileModel.objects.all()
    serializer_class = FileModelSerializer
    
    def get(self, request, pk, pk2):
        user_profile = ProfileModel.objects.filter( user_mail_id = pk).latest("id")
        user_producttype = ProductType.objects.get(id = pk2)
        return_data = []

        if user_producttype.id == user_profile.product_type_id:
            items = user_producttype.items
            all_file = self.queryset.filter( user_mail_id = pk, product_type_id = pk2)
            return_value = []

            for i in range( items):
                temp = all_file.filter( items = i).order_by('order')
                serializer = FileModelSerializer( temp, many=True)
                return_value.append( serializer.data)
           
            return Response (tuple(return_value))

