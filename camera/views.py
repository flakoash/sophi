from django.shortcuts import render
import base64
import re
import requests
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from camera.models import *
from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


def camera(request):
    return render(request, 'camera/camera.html', {})

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
        cam = photos()
        cam.user = request.user
        cam.photo = img64
        cam.save()
        data = {'photo': img64}
        #r = requests.post(url, data=json.dumps(data), headers=headers)
        return Response({'saved': 'ok'})

@csrf_exempt
def ajaxupload(request):
    url = "http://localhost:8000/raspberry_rest/"
    headers = {'content-type': 'application/json'}
    img64=request.POST['imgBase64']
    print(len(img64))
    #f = open("temp.png", "w")
    #f.write(img64)
    #f.close()
    #ImageData = base64.b64decode(img64)
    cam=photos()
    cam.user=request.user
    cam.photo=img64
    cam.save()
    data={'photo':img64}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return JsonResponse({'saved':'ok'})



