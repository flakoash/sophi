from django.shortcuts import render
import re
import requests
import json
from django.http import JsonResponse
import io, base64
#from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from camera.models import *
from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

# Create your views here.
@csrf_exempt
class camera(APIView):
    parser_classes = (FileUploadParser,)
    def post (self, request, filename, format=None ):
        #print(request.POST)
        print(request.data['file'])
        #img64 = request.FILES['file']
        print(request.FILES)
        #print(request.POST)
        #print('len: '+str(len(img64))+' type: '+str(type(img64))+' : '+str(img64))
        #print(type(img64))
        #print(img64)
        return JsonResponse({'saved': 'ok'})


class cameraview(APIView):
    #authentication_classes = (JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        return render(request,'camera/camera.html')
    def post(self, request, format=None):
        url = "http://localhost:8000/raspberry_rest/"
        headers = {'content-type': 'application/json'}
        img64 = request.POST['imgBase64']
        print(len(img64))
        # f = open("temp.png", "w")
        # f.write(img64)
        # f.close()
        # ImageData = base64.b64decode(img64)
        #cam = photos()
        #cam.user = request.user
        #cam.photo = img64
        #cam.save()
        #data = {'photo': img64}
        #r = requests.post(url, data=json.dumps(data), headers=headers)
        return Response({'len': print(len(img64)),'type':type(img64)})


@csrf_exempt
def ajaxupload(request):
    url = "http://localhost:8000/raspberry_rest/"
    headers = {'content-type': 'application/json'}
    #img64=request.POST['imgBase64']
    #image_data = base64.b64decode(re.search(r'base64,(.*)', request.POST['imgBase64']).group(1))
    #print(image_data)


    a = base64.b64decode(img64)
    #cam=photos()
    #cam.user=request.user
    #cam.photo=img64
    #cam.save()
    #data={'photo':img64}
    #r = requests.post(url, data=json.dumps(data), headers=headers)
    return JsonResponse({'saved':'ok'})



