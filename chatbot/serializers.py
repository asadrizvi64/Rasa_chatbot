from rest_framework.serializers import ModelSerializer
from .models import *


class PolicyInformationSerializer(ModelSerializer):
    class Meta:
        model = PolicyInformation
        fields = '__all__'