from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny 
from .models import VerifyType, ProductType, NationType, StoreType, Category, EntryType
from .serializer import VerifyTypeSerializer, ProductTypeSerializer, NationTypeSerializer, StoreTypeSerializer, CategorySerializer, EntryTypeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

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
        
