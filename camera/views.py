from django.shortcuts import render
import base64
import re
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def camera(request):
    return render(request, 'camera/camera.html', {})

@csrf_exempt
def ajaxupload(request):
    img64=request.POST['imgBase64']
    #print(img64)
    f = open("temp.png", "w")
    f.write(img64)
    f.close()
    #ImageData = base64.b64decode(img64)
    return JsonResponse({'saved':'ok'})


