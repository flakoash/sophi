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

from SOPHINET.BAGS import BAGS
from SOPHINET.SHOES import SHOES
from SOPHINET.DOWNBODY import DOWNBODY
from SOPHINET.UPPERBODY import UPPERBODY
from camera.GoogleVisionClass import GoogleVision

dummy=['shirt','short','jeans','underwear','pants']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bags = BAGS(False, BASE_DIR+'/SOPHINET/GRAPHS/'+'BAGS')
upperbody = UPPERBODY(False, BASE_DIR+'/SOPHINET/GRAPHS/'+'UPPERBODY')
downbody = DOWNBODY(False, BASE_DIR+'/SOPHINET/GRAPHS/'+'DOWNBODY')

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
        filename = BASE_DIR + '/photos/some_image' + str(ph.id) + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        ''' L1. Google Cloud Vision '''
        print('google vision ....')
        #gglv = GoogleVision(filename)
        labels = [('something', 0.01)] #gglv.predict()

        clothe = True

        print('sophinet ...')
        ''' L2. SOPHI '''
        #nn = SOPHINET(image_path = filename, class_ = 'SHOES', n_top_picks = 5, verbosity = False)
        #logits = {class_: prob_ for class_, prob_ in nn.predict()}
        
        shoes = SHOES(False, BASE_DIR+'/SOPHINET/GRAPHS/'+'SHOES')

        l0 = shoes.predict(filename)
        l1 = [('d', 0.05)] #upperbody.predict(filename)
        l2 = [('a', 0.2)] #downbody.predict(filename)
        l3 = [('e', 0.3)] #bags.predict(filename)

        print(labels, l0, l1, l2, l3)
        l_ = labels+l0+l1+l2+l3

        human_strings = [each[0] for each in l_]
        scores = [each[1] for each in l_]

        for i in range(len(human_strings)):
            for j in range(len(human_strings)-1):
                if scores[i] > scores[j]:
                    aux = scores[j]
                    scores[j] = scores[i]
                    scores[i] = aux
                    aux = human_strings[j]
                    human_strings[j] = human_strings[i]
                    human_strings[i] = aux

        max_ = max(scores)
        index_ = scores.index(max_)

        most_likely = [each for each in human_strings[:5]]
        print(most_likely)

        ph.photo = filename
        ph.save()
        json_ = {
        'message': "image uploaded",
        'data' : {
        'isClothe' : clothe,
        'mostLikely' : human_strings[index_],
        'otherPossibilities' : [most_likely[0], most_likely[1], most_likely[2]]
        }
        }

        print(json_)
        return JsonResponse(json_)

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

