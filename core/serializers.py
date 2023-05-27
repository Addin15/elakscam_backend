from rest_framework import serializers

from users.serializers import UserSerializer

class ReportSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    account_number = serializers.CharField()
    category = serializers.CharField()
    evidence = serializers.FileField(required=False)
    evidence_description = serializers.CharField(required=False)
    reported_by = UserSerializer(read_only=True)
    datetime = serializers.DateTimeField(read_only=True)

class AccountSerializer(serializers.Serializer):
    number = serializers.CharField()
    holder_name = serializers.CharField()
    appealed = serializers.BooleanField()