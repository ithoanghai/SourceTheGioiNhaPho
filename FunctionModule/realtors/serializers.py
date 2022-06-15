from rest_framework import serializers

from FunctionModule.realtors.models import Realtor


class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtor
        exclude = ()
        read_only_fields = ()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
