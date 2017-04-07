from django.shortcuts import render
import base64
import re
import requests
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from camera.models import *

# Create your views here.

def camera(request):
    return render(request, 'camera/camera.html', {})

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


