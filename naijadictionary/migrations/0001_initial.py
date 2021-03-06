# Generated by Django 2.2.5 on 2020-02-14 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20, unique=True)),
                ('meaning', models.CharField(max_length=1000)),
                ('country', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolio_url', models.CharField(blank=True, max_length=100)),
                ('d_o_b', models.DateField(null=True)),
                ('gender', models.BooleanField(null=True)),
                ('location', models.CharField(max_length=20, null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profilepic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submited',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, null=True)),
                ('word', models.CharField(max_length=20, null=True, unique=True)),
                ('meaning', models.CharField(max_length=1000)),
                ('language', models.CharField(max_length=20)),
                ('exampe', models.CharField(max_length=200)),
                ('post_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to='naijadictionary.UserProfile')),
            ],
        ),
    ]
