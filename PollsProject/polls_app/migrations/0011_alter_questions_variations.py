# Generated by Django 3.2.7 on 2021-09-25 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0010_alter_answers_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='variations',
            field=models.ManyToManyField(blank=True, null=True, to='polls_app.Variation', verbose_name='Варианты'),
        ),
    ]
