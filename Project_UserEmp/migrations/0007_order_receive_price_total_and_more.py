# Generated by Django 4.1.7 on 2023-02-24 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project_UserEmp', '0006_alter_order_payment_pay_date_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_receive',
            name='price_total',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='order_payment',
            name='order_rec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project_UserEmp.order_receive', unique=True),
        ),
    ]
