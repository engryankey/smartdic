# Generated by Django 2.2.5 on 2020-02-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naijadictionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=8, null=True),
        ),
    ]