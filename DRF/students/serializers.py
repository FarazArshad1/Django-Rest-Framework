from rest_framework import serializers

class StudentSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    batch = serializers.IntegerField()
    roll_number = serializers.CharField(max_length=25)
    city = serializers.CharField(max_length=100)

    