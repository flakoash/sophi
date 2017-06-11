import re, json, io, base64, os
from PIL import Image
from random import randint

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

from camera.models import *

from rest_framework.decorators import authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from SOPHINET.SOPHINET_class import SOPHINET
from camera.GoogleVisionClass import GoogleVision

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
    # authentication_classes = (JSONWebTokenAuthentication)
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        #return render(request, 'camera/camera.html')
        return render(request, 'PostMultiPartImage.html')

    def post(self, request, format=None):
        dst = 'C:/Users/HP/Dropbox/SOPHI/SOPHIBackend/photos'

        ''' Handle File '''
        file = request.FILES['file']
        #print( 'Url upladed file: ', file.name )
        fs = FileSystemStorage()
        _ = fs.save(file.name, file)
        image_path = dst+'/'+file.name

        ''' Predict class (Two layer flow) '''
        
        ''' L1. Google Cloud Vision '''
        gglv = GoogleVision(image_path)
        labels = gglv.predict()

        ''' L2. SOPHI '''
        nn = SOPHINET(image_path = image_path, class_ = 'SHOES', n_top_picks = 5, verbosity = False)
        logits = {class_: prob_ for class_, prob_ in nn.predict()}
        #logits = {a:b for a,b in [('a',0.5),('b',0.8),('c',0.9)]}
        
        print('-------------------------GOOGLE VISION---------------------')
        print(labels)
        print('------------------------------------------------------------')
        print('---------------------------SOPHINET-------------------------')
        print(logits)
        print('------------------------------------------------------------')

        ''' Response '''

        '''{
            data: {
                isClothe: true
                classes: []
            }
        }'''

        return JsonResponse({'data': {'isClothe': True, 'classes': labels} })

@method_decorator(csrf_exempt, name='dispatch')
class cameraimage2(APIView):
    # authentication_classes = (JSONWebTokenAuthentication)
    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        #return render(request, 'camera/camera.html')
        return render(request, 'PostMultiPartImage.html')

    def post(self, request, format=None):
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
        print(BASE_DIR)
        filename = BASE_DIR + '/photos/some_image' + str(ph.id) + '.png'

        with open(filename, 'wb') as f:
            f.write(imgdata)  # print(request.data)

        ''' L1. Google Cloud Vision '''
        print('google vision ....')
        gglv = GoogleVision(filename)
        labels = gglv.predict()

        print('sophinet ...')
        ''' L2. SOPHI '''
        '''nn = SOPHINET(image_path = filename, class_ = 'SHOES', n_top_picks = 5, verbosity = False)
        logits = {class_: prob_ for class_, prob_ in nn.predict()}
        labels = []
        print('done!')
        list = [ str(str(value)+":"+str(key)) for value, key in logits.items() ]
        labels.append(list)'''

        ph.photo = filename
        ph.save()
        print(ph.photo.url)
        print(labels)
        return JsonResponse({'classes': labels, 'url': ph.photo.url})

@method_decorator(csrf_exempt, name='dispatch')
class cameraviewdummy(APIView):
    #authentication_classes = (JSONWebTokenAuthentication)
    #permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        #return JsonResponse({'result':'ok'})
        return render(request,'camera/camera.html')
    def post(self, request, format=None):
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
        print(BASE_DIR)
        filename = BASE_DIR + '/photos/some_image' + str(ph.id) + '.png'

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
    #print(djangota)
    data = data.replace('data:image/png;base64,', '')
    #print(data)
    imgdata = base64.b64decode(data)
    print (BASE_DIR)
    filename = BASE_DIR+'/photos/some_image'+str(ph.id)+'.png'

    with open(filename, 'wb') as f:
        f.write(imgdata)  # print(request.data)


    ph.photo = filename
    ph.save()
    print(ph.photo.url)
    classes={}
    #nn=SOPHI_net(image_path=BASE_DIR+"/Share_NN_models/test1.jpg",n_top_picks=5,verbosity=True,dir_path=BASE_DIR+"/Share_NN_models/")
    #classes=nn.predict()
    print(classes)
    return JsonResponse({'clases': str(classes), 'url': ph.photo.url})
