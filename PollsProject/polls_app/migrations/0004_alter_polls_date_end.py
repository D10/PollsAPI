# Generated by Django 3.2.7 on 2021-09-24 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0003_auto_20210924_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polls',
            name='date_end',
            field=models.DateTimeField(verbose_name='Дата окончания'),
        ),
    ]
