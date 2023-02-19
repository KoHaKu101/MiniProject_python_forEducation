# Generated by Django 4.1.7 on 2023-02-19 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project_UserEmp', '0003_alter_employee_img_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='tooltype',
            fields=[
                ('tooly_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tooly_name', models.CharField(max_length=100, unique=True)),
                ('tooly_status', models.BooleanField(default='True')),
                ('tooly_des', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tool',
            fields=[
                ('tool_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tool_name', models.CharField(max_length=100, unique=True)),
                ('tool_price', models.BooleanField(default='True')),
                ('tool_des', models.TextField(blank=True, default='', null=True)),
                ('tool_img', models.ImageField(blank=True, default='', null=True, upload_to='static/images/employee/')),
                ('tool_type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Project_UserEmp.tooltype')),
            ],
        ),
    ]