# Generated by Django 4.1.7 on 2023-04-18 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0031_alter_beacon_x_alter_beacon_y_alter_beacon_z'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beacon',
            name='question_area1_strength',
            field=models.IntegerField(default=0, verbose_name='questionarea1_strength'),
        ),
    ]
