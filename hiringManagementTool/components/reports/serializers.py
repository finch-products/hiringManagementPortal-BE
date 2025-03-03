from rest_framework import serializers

class AgedemandReportSerializer(serializers.Serializer):
    age = serializers.CharField()
    count = serializers.IntegerField()

class OpenDemandSerializer(serializers.Serializer):
    total_open_demands = serializers.IntegerField()
    total_non_open_demands = serializers.IntegerField()
    total_india_open_demands = serializers.IntegerField()
    total_non_india_open_demands = serializers.IntegerField()

class TotalPositionsOpenedLastWeekSerializer(serializers.Serializer):
    total_positions_opened_last_week = serializers.IntegerField()

class DemandFulfillmentMetricsSerializer(serializers.Serializer):
    open_positions = serializers.DecimalField(max_digits=5, decimal_places=2)
    profiles_submitted = serializers.DecimalField(max_digits=5, decimal_places=2)
    interview_scheduled = serializers.DecimalField(max_digits=5, decimal_places=2)
    profiles_not_submitted = serializers.DecimalField(max_digits=5, decimal_places=2)
