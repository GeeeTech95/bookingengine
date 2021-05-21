from rest_framework import serializers 
from .models import Listing

class ListingSerializer(serializers.ModelSerializer) :

    class Meta() :
        model = Listing
        fields = ['listing_type','title','country','city','price']