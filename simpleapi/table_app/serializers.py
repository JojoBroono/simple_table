from rest_framework import serializers


class TableRowSerializer(serializers.Serializer):
    dt = serializers.DateField()
    name = serializers.CharField(max_length=1000)
    amount = serializers.IntegerField()
    distance = serializers.IntegerField()