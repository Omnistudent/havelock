# Generated by Django 4.2 on 2023-04-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0035_alter_question_answer1_english_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='area4',
            field=models.CharField(default='area4', max_length=300, verbose_name='area4'),
        ),
        migrations.AddField(
            model_name='question',
            name='area5',
            field=models.CharField(default='area5', max_length=300, verbose_name='area5'),
        ),
        migrations.AlterField(
            model_name='question',
            name='area3',
            field=models.CharField(default='area3', max_length=300, verbose_name='area3'),
        ),
    ]