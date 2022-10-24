from http.client import HTTPResponse
from django.shortcuts import render
from .models import UserVerifyModel, ProfileModel
from setups.models import ProductType, VerifyType, StoreType, NationType, Category
from .serializer import UserVerifyModelSerializer, ProfileModelSerializer
from setups.serializer import NationTypeSerializer, StoreTypeSerializer, CategorySerializer, ProductTypeSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from rest_framework import status
import json


class UserVerifyView2( generics.GenericAPIView):
    permission_classes = [AllowAny]
    queryset = UserVerifyModel.objects.all()
    serializer_class = UserVerifyModelSerializer

    # def post(self, request):
    #     print (request.data)
    #     return Response({"test":"works"})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)  

# Create your views here.
class UserVerifyView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserVerifyModelSerializer
    queryset = UserVerifyModel.objects.all()

    @action(detail=False, methods=['post'], url_path='user-info')
    def user_info( self, request):

        # verification with email and phone
        verify_by = VerifyType.objects.last()
        verify_by_email = verify_by.email_verify
        verify_by_phone = verify_by.phone_verify
        ver_user = None
        temp_email = request.data.get("user_mail")
        temp_phone = request.data.get("user_phone")

        try:    
            ver_user_email = UserVerifyModel.objects.filter(user_mail=temp_email).order_by('-id')[0]
        except:
            ver_user_email = None       
        try:
            ver_user_phone = UserVerifyModel.objects.filter(user_phone=temp_phone).order_by('-id')[0]
        except:
            ver_user_phone = None
        if (verify_by_email == True and verify_by_phone == False) and (ver_user_email != None):
            ver_user =  ver_user_email
        elif (verify_by_phone == True and  verify_by_email == False) and (ver_user_phone != None):
            ver_user =  ver_user_phone
        elif (verify_by_phone == True and  verify_by_email == True) and (ver_user_email != None) and (ver_user_phone != None) and (ver_user_email == ver_user_phone):
            ver_user =  ver_user_email
        else:
            ver_user =  None
        if ver_user != None:
            serializer = UserVerifyModelSerializer( ver_user, many=False)
            return Response( serializer.data)
        return HttpResponseNotFound()


# Create your views here.
class ProfileView( viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProfileModelSerializer
    queryset = ProfileModel.objects.all()

    @action(detail=True, methods=['GET'], url_path='cur-profile')
    def user_data( self, request, pk):
        try:
            user_queryset = self.queryset.filter(user_mail_id=pk)
        except:
            user_queryset = None

        if len( user_queryset) > 0:
            temp_user = user_queryset[0]
            serializer = ProfileModelSerializer( temp_user, many=False)
            return Response( serializer.data)
        else:
            ###------ make new profile if there is no
            cur_user = UserVerifyModel.objects.get(id=pk)
            temp = ProfileModel.objects.create(primary_key=True, user_mail = cur_user)

    @action(detail=True, methods=['PATCH'], url_path='put-profile')
    def put_profile( self, request, pk):
        user_queryset = self.queryset.filter(pk=pk)[0]
        serializer = ProfileModelSerializer( user_queryset, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
        else:
            print ("not")
        return Response( serializer.data)
       

    @action(detail=True, methods=['PATCH'], url_path='put-step')
    def put_step( self, request, pk):

        user_queryset = self.queryset.filter(pk=pk)[0]
        user_queryset.process_step = request.data.get('process_step')

        serializer = ProfileModelSerializer( user_queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return
        return Response( serializer.data)

















        # if len( user_queryset) > 0:
        #     temp_user = user_queryset[0]
        #     serializer = ProfileModelSerializer( temp_user, many=False)
        #     return Response( serializer.data)
        # else:
        #     ###------ make new profile if there is no
        #     cur_user = UserVerifyModel.objects.get(id=pk)
        #     temp = ProfileModel.objects.create(primary_key=True, user_mail = cur_user)