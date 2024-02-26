# Generated by Django 4.2.9 on 2024-02-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_booking_selected_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='description',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]