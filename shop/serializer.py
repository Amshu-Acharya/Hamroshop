from unicodedata import category

from rest_framework.serializers import ModelSerializer



class CategorySerializer(ModelSerializer):
    class Meta:
        model = category
        fields ='__all__'

