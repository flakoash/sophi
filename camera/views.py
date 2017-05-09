from django.shortcuts import render
import re
import json
from django.http import JsonResponse
import io, base64

from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from camera.models import *
from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from random import randint
import os

dummy=['shirt','short','jeans','underwear','pants']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
           return None

        return (user, None)

class camera(APIView):

    #authentication_classes = (UnsafeSessionAuthentication,)
    parser_classes = (FileUploadParser,)

    def post(self, request, filename="asd.jpg", format=None):
        print("camera")
        file_obj = request.POST
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)
    def get(self,request, format=None):
        return render(request,'camera/camera.html')


@method_decorator(csrf_exempt, name='dispatch')
class cameraview(APIView):

    #authentication_classes = (JSONWebTokenAuthentication)
    #permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        return render(request,'camera/camera.html')
    def post(self, request, format=None):
        print("cameraview")
        #print(request.body)
        data = request.body.decode("utf-8")
        json_acceptable_string = data.replace("'", "\"")
        data = json.loads(json_acceptable_string)
        #print(type(data))
        data = data['image'].replace(' ', '+')
        # print(data)
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += '=' * (4 - missing_padding)
        #print(data)
        data = data.replace('data:image/png;base64,', '')
        # print(data)
        imgdata = base64.b64decode(data)
        filename = 'some_image.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)  # print(request.data)
        return JsonResponse({'saved': 'ok'})

@method_decorator(csrf_exempt, name='dispatch')
class cameraviewdummy(APIView):

    #authentication_classes = (JSONWebTokenAuthentication)
    #permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        return render(request,'camera/camera.html')
    def post(self, request, format=None):
        print("cameraviewdummy")
        ph = photos()
        ph.save()
        #print(request.body)
        data = request.body.decode("utf-8")
        json_acceptable_string = data.replace("'", "\"")
        data = json.loads(json_acceptable_string)
        #print(type(data))
        data = data['image'].replace(' ', '+')
        # print(data)
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += '=' * (4 - missing_padding)
        #print(data)
        data = data.replace('data:image/png;base64,', '')
        # print(data)
        imgdata = base64.b64decode(data)
        filename = 'photos/some_image' + str(ph.id) + '.png'
        print(filename)
        with open(filename, 'wb') as f:
            f.write(imgdata)  # print(request.data)

        ph.photo = filename
        ph.save()
        print(ph.photo.url)
        return JsonResponse({'clases': dummy[randint(0, 4)], 'url': ph.photo.url})

@csrf_exempt
def ajaxupload(request):
    print("ajaxupload")
    ph = photos()
    ph.save()
    #print(request.POST)
    data = request.POST['imgBase64'].replace(' ', '+')
    #print(data)
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    #print(data)
    data = data.replace('data:image/png;base64,', '')
    #print(data)
    imgdata = base64.b64decode(data)
    filename = 'photos/some_image'+str(ph.id)+'.png'

    with open(filename, 'wb') as f:
        f.write(imgdata)  # print(request.data)


    ph.photo = filename
    ph.save()
    print(ph.photo.url)
    return JsonResponse({'clases': dummy[randint(0, 4)], 'url': ph.photo.url})

