# Generated by Django 3.2.7 on 2021-09-24 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0009_auto_20210925_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='polls_app.questions', verbose_name='Вопрос'),
        ),
    ]