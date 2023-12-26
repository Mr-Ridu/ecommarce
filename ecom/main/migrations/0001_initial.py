# Generated by Django 4.2.2 on 2023-08-06 08:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cartProductitems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('CPname', models.CharField(max_length=150)),
                ('CPpicture', models.ImageField(blank=True, null=True, upload_to='cart_picture')),
                ('ProductID', models.IntegerField()),
                ('CPrice', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pvendorname', models.CharField(max_length=100)),
                ('Pname', models.CharField(max_length=100)),
                ('Ppicture', models.ImageField(blank=True, null=True, upload_to='product_picture')),
                ('Pdesc', models.CharField(max_length=1000)),
                ('Pstock', models.IntegerField()),
                ('Pprice', models.IntegerField()),
                ('Pmallname', models.CharField(max_length=100)),
                ('Pcatg', models.CharField(max_length=100)),
                ('product_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Product Code')),
            ],
        ),
        migrations.CreateModel(
            name='PurchesDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('PPname', models.CharField(max_length=100)),
                ('PPid', models.IntegerField()),
                ('Pfirstname', models.CharField(max_length=100)),
                ('Plastname', models.CharField(max_length=100)),
                ('Pmobile', models.IntegerField()),
                ('Pemail', models.EmailField(max_length=254)),
                ('Padderss', models.CharField(max_length=100)),
                ('Pzipcode', models.IntegerField()),
                ('Pdivision', models.CharField(max_length=100)),
                ('Pcity', models.CharField(max_length=100)),
                ('Parea', models.CharField(max_length=100)),
                ('Pdeliverytyp', models.CharField(max_length=100)),
                ('product_code', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Product Code')),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
