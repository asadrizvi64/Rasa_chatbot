from rest_framework.serializers import ModelSerializer
from .models import *


class PolicyInformationSerializer(ModelSerializer):
    class Meta:
        model = PolicyInformation
        fields = '__all__'


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ResponsesSerializer(ModelSerializer):
    class Meta:
        model = Responses
        fields = '__all__'


class ContractorSerializer(ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'


class InsuranceTypeSerializer(ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = '__all__'


class DefinitionSerializer(ModelSerializer):
    class Meta:
        model = Definition
        fields = '__all__'


class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class SlotSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'