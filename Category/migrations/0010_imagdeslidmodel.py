# Generated by Django 4.1.4 on 2022-12-09 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0009_alter_imageproductmodel_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagdeSlidModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(upload_to='')),
                ('image3', models.ImageField(upload_to='')),
            ],
        ),
    ]