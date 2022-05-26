from rest_framework import serializers
from .models import Realtor


class RealtorSerializer(serializers.ModelSerializer):
    listings = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='listing-detail',
                                                lookup_field='listing_id')
    #  Mandatory for UUID serialization
    realtor_id = serializers.UUIDField()

    class Meta:
        model = Realtor
        exclude = ('id', 'password')
        read_only_fields = ('created', 'username', 'listings',)
