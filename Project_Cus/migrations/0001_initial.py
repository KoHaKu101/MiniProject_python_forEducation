# Generated by Django 4.1.7 on 2023-02-20 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('sur_name', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('address', models.TextField(default='', null=True)),
                ('subdistrict', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('Province', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('tel', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=32)),
            ],
        ),
    ]