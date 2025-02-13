from hiringManagementTool.models.candidates import CandidateMaster
from rest_framework import serializers

class CandidateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateMaster
        fields = '__all__'