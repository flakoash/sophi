"""sophi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from camera import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from camera.viewsets import UploadImageViewSet

router = routers.DefaultRouter()
router.register('images', UploadImageViewSet, 'images')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^camera$', views.camera.as_view()),
    url(r'^asd$', views.ajaxupload,name="uploadphoto"),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^image/', views.cameraview.as_view()),
    url(r'dummy^$', views.cameraviewdummy.as_view()),
    url(r'^$', views.cameraimage2.as_view())
    #url(r'^', include(router.urls)),

    #curl -X POST -H "Content-Type: application/json" -d '{"username":"qwerty","password":"qwerty"}' http://localhost:8000/api-token-auth/
    #curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoicXdlcnR5IiwiZXhwIjoxNDkxNzUyMzI4fQ.Pyqug0pe5s5ApT3qcd-Z62J9Tg3YLno7NI12g13k8YM"}' http://localhost:8000/api-token-verify/
    #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoicXdlcnR5IiwiZXhwIjoxNDkxNzUyMzI4fQ.Pyqug0pe5s5ApT3qcd-Z62J9Tg3YLno7NI12g13k8YM
    #curl -H "Authorization: JWT <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6IiIsInVzZXJuYW1lIjoicXdlcnR5IiwiZXhwIjoxNDkxNzUyMzI4fQ.Pyqug0pe5s5ApT3qcd-Z62J9Tg3YLno7NI12g13k8YM>" http://localhost:8000/secure/
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
