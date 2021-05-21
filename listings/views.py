from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Listing,Booked,HotelRoomType,HotelRoom
from .serializers import ListingSerializer
from django.db.models import Q
from django.http import HttpResponse
from itertools import chain
from datetime import date
import operator




@api_view(['GET'])
def get_available(request) :
    if request.method == 'GET' :
        check_in = request.GET.get('check_in',None)
        check_out  = request.GET.get('check_out',None)
        max_price = request.GET.get('max_price',None)
        if not check_in or not check_out or not max_price :
            return HttpResponse('incomplete request parameters',status = 400)

        check_in = check_in.split('-') 
        check_out = check_out.split('-')  
        try : 
            year_out = int(check_out[0])
            month_out = int(check_out[1])
            day_out = int(check_out[2])

            year_in = int(check_out[0])
            month_in = int(check_out[1])
            day_in = int(check_out[2]) 
        
            check_out = date(year = year_out,month = month_out,day = day_out) 
            check_in = date(year = year_in,month = month_in,day = day_in) 
 
        except  (IndexError,TypeError) :
            return HttpResponse("incomplete request parameters",status = 400)
        try : max_price = int(max_price)
        except TypeError : 
            return HttpResponse("incomplete request parameters",status = 400)
        booked_apartment = Booked.objects.filter(start_date__gte = check_in,
        end_date__lte = check_out).values_list('apartment__id')   
        apartment_listings = Listing.objects.filter(price__lte = max_price,listing_type = 'apartment').exclude(id__in = booked_apartment)
    
        booked_rooms = Booked.objects.filter(start_date__gt = check_in,
        end_date__lt = check_out).values_list('hotel_room__id') 
        
        avail_rooms = HotelRoom.objects.filter(hotel_room_type__price__lte = max_price).exclude(id__in = booked_rooms)
   
        hotel_listings = []
        for room in avail_rooms :
            if room.hotel_room_type.hotel not in hotel_listings :
                #setting the price of hotel histing to price of already ordered set
                setattr(room.hotel_room_type,'price',room.hotel_room_type.price)
                hotel_listings.append(room.hotel_room_type.hotel)  
       
        results = list(chain(apartment_listings,hotel_listings))
        results = sorted(results,key=operator.attrgetter('price'))
        serialized = ListingSerializer(results,many=True)
    else : 
        return HttpResponse("invalid request type",status = 400)

    return Response(serialized.data)
