# Generated by Django 3.2 on 2021-05-17 20:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20210517_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinginfo',
            name='booking_end',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookinginfo',
            name='booking_start',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookinginfo',
            name='hotel_room',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_info', to='listings.hotelroom'),
        ),
        migrations.CreateModel(
            name='Booked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
                ('hotel_room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='listings.hotelroom')),
            ],
        ),
    ]