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

class LobTargetProgressSerializer(serializers.Serializer):
    LOB_name = serializers.CharField() # Adjust max_length as needed
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

class DemandByStatusSerializer(serializers.Serializer):
    category = serializers.CharField()
    LOB = serializers.JSONField()
    total = serializers.IntegerField()

class ClientSelectionPercentageSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    selection_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

class demandTimeTakenSerializer(serializers.Serializer):
    demand_id = serializers.CharField()
    time_taken = serializers.IntegerField()

class AverageTimeTakenbyClientsSerializer(serializers.Serializer):
    client_name = serializers.CharField()
    time_taken = serializers.IntegerField()

class ReportSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    report = serializers.DictField()

class OpenPositionSerializer(serializers.Serializer):
    department_name = serializers.CharField()
    lob_name = serializers.CharField()
    open_positions = serializers.IntegerField()