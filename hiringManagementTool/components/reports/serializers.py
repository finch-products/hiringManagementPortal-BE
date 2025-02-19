from rest_framework import serializers

class AgedemandReportSerializer(serializers.Serializer):
    age = serializers.CharField()
    count = serializers.IntegerField()