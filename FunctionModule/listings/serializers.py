from rest_framework import serializers
from .models import Listing, Realtor

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

class ListingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Listing 
        #fields =  '__all__' 
        fields = ('id', 'address', 'area', 'area_unit', 'bathrooms','bedrooms','code','description','direction','district','extra_data','floors',
                    'house_type', 'registration_type', 'lane_width', 'length', 'list_date','location','lot_size', 
                    'price','sale_price','road_type','state','status','street','title','urban_area','transaction_type',
                    'ward','width','is_exclusive','is_published','is_verified')
        #, 'listingimage', 'listingvideo'

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
