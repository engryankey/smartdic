# Generated by Django 2.2.5 on 2020-02-19 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijadictionary', '0004_auto_20200218_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='definition',
            name='language',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='submited',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
