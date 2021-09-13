from rest_framework.serializers import ModelSerializer
from .models import CustomImage


class CustomImageSerializer(ModelSerializer):
    class Meta:
        model = CustomImage
        fields = ('id', 'file', 'file_name')
