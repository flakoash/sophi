from rest_framework import viewsets
from camera.serializers import UploadImageSerializer
from camera.models import photos

class UploadImageViewSet(viewsets.ModelViewSet):
    queryset = photos.objects.all()
    serializer_class = UploadImageSerializer