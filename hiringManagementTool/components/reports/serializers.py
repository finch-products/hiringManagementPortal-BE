from rest_framework import serializers

class AgedemandReportSerializer(serializers.Serializer):
    age = serializers.CharField()
    count = serializers.IntegerField()

class OpenDemandSerializer(serializers.Serializer):
    total_open_demands = serializers.IntegerField()
    total_non_open_demands = serializers.IntegerField()
    total_india_open_demands = serializers.IntegerField()
    total_non_india_open_demands = serializers.IntegerField()
