# Generated by Django 4.1.7 on 2023-02-23 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_UserEmp', '0005_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_payment',
            name='pay_date_send',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
