# Generated by Django 4.2.9 on 2024-02-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_class_canceled_class_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
