# Generated by Django 4.2.2 on 2023-08-08 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_productdetails_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetails',
            name='product_code',
            field=models.CharField(editable=False, max_length=15, unique=True),
        ),
    ]
