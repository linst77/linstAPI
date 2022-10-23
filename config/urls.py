"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from users.views import UserVerifyView, ProfileView, UserVerifyView2
from setups.views import VerifyTypeView, ProductTypeView, NationTypeView, StoreTypeView, CategoryView, EntryTypeView
from content.views import ContentModelView, FileModelView, FileUserListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    path('api/files/<int:pk>/<int:pk2>/', FileUserListView.as_view(), name='user_files'),
    path('api/user/', UserVerifyView2.as_view(), name='user_api')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

router = DefaultRouter()
router.register('userverify', UserVerifyView, basename='api_userverify')
router.register('profile', ProfileView, basename='api_profile')

router.register('producttype', ProductTypeView, basename='api_producttype')
router.register('nation', NationTypeView, basename='api_nation')
router.register('store', StoreTypeView, basename='api_store')
router.register('category', CategoryView, basename='api_category')
router.register('entry', EntryTypeView, basename='api_entry')



router.register('content', ContentModelView, basename='api_product')
router.register('file', FileModelView, basename='api_file')
urlpatterns += router.urls