# Generated by Django 4.1.4 on 2022-12-09 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_remove_otpcodemodel_phone_otpcodemodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcodemodel',
            name='code',
            field=models.CharField(max_length=500, null=True),
        ),
    ]