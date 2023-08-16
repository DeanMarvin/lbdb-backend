from rest_framework import serializers
from desks.models import Desks


class Desk(object):
    def __init__(self, d_id, name, client, licence, active):
        self.d_id = d_id
        self.name = name
        self.client = client
        self.licence = licence
        self.active = active


class DeskUpdateSerializer(serializers.Serializer):
    d_id = serializers.IntegerField()
    name = serializers.CharField()
    client = serializers.CharField()
    licence = serializers.BooleanField()
    active = serializers.BooleanField()

    def update(self, validated_data):
        return Desk(**validated_data)


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desks
        fields = ["d_id", "name", "client", "licence", "active"]

    def validate_desk(self, data):
        return data
