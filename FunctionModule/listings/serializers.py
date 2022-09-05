from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Listing 
        #fields =  '__all__' 
        fields = ('id', 'address', 'area', 'area_unit', 'bathrooms','bedrooms','code','description','direction','district','extra_data','floors',
                    'house_type', 'registration_type', 'lane_width', 'length', 'date_created','location','lot_size',
                    'price','sale_price','road_type','state','status','street','title','urban_area','transaction_type',
                    'ward','width','is_exclusive','is_published','is_verified')
        #, 'listingimage', 'listingvideo'

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
