from rest_framework import serializers
from camera.models import photos
class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = photos
        fields = ('pk','photo',)