# Generated by Django 4.1.7 on 2023-02-23 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_UserEmp', '0002_setting_default_rename_emp_id_repair_detail_emp'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_receive',
            name='price_service',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
