# Generated by Django 2.2 on 2020-03-14 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20200314_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='access',
            field=models.CharField(choices=[('general', 'Общий'), ('hidden', 'Скрытый'), ('private', 'Приватный')], default='general', max_length=20, verbose_name='Общий доступ'),
        ),
    ]
