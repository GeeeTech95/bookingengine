from django.db import models


class Listing(models.Model):
    HOTEL = 'hotel'
    APARTMENT = 'apartment'
    LISTING_TYPE_CHOICES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
    )

    listing_type = models.CharField(
        max_length=16,
        choices=LISTING_TYPE_CHOICES,
        default=APARTMENT
    )
    title = models.CharField(max_length=255,)
    country = models.CharField(max_length=255,)
    city = models.CharField(max_length=255,)
    #new
    price = models.FloatField(blank = True,null = True) #allowed blank in case of listing type being a hotel

    def __str__(self):
        return self.title

    class Meta() :
        ordering = ['-price']     


    

class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=False,
        null=False,       #changed to False,we need a hotel to tie to a room type.
        on_delete=models.CASCADE,
        related_name='hotel_room_types'
    )
    title = models.CharField(max_length=255,)
    #new
    price = models.FloatField()  

    def __str__(self):
        return f'{self.hotel} - {self.title}'


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='hotel_rooms'
    )
    room_number = models.CharField(max_length=255,)

    def __str__(self):
        return self.room_number

    class Meta() :
        ordering = ['hotel_room_type__price']



class BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info'
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    #new
    hotel_room = models.OneToOneField(
        HotelRoom,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='booking_info',
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    """we can automatically block days once a booking info is saved
    so i will overide the save method here,so i added new fields,to enable that"""
    #new
    booking_start = models.DateField() 
    booking_end = models.DateField()


    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type
            
        return f'{obj} {self.price}'
    
    #new
    def save(self,*args,**kwargs)  :
        if self.listing :
            if not Booked.objects.filter(apartment = self.listing,is_active = True).exists() :
                Booked.objects.create(apartment = self.listing,
                start_date = self.booking_start,
                end_date = self.booking_end
                )

        elif self.hotel_room :
            if not Booked.objects.filter(hotel_room= self.hotel_room,is_active = True).exists() :
                Booked.objects.create(hotel_room = self.hotel_room,
                start_date = self.booking_start,
                end_date = self.booking_end
                )



        super(BookingInfo,self).save(*args,**kwargs)  



class Booked(models.Model) :
    """ could also make it OneToOneField but for the pupose of keeping booking data,
    for future purposes i made it foreign key,will use another field to know active ones"""
    
    apartment = models.ForeignKey(Listing,
                on_delete= models.CASCADE,null = True,
                blank = False,related_name = 'booked_apartment')
    hotel_room = models.ForeignKey(HotelRoom,on_delete= models.CASCADE,
    null = True,related_name  = 'booked_hotel_room',
    blank = False)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default  = True) #in active bookings are not valid for booked

    def __str__(self) :
        
        if self.apartment :
            obj = self.apartment
        else:
            obj = self.hotel_room
            
        return f'{obj} {self.start_date} {self.end_date}' 