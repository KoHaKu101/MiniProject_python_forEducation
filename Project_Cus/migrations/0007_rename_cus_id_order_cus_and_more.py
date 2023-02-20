# Generated by Django 4.1.7 on 2023-02-20 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project_Cus', '0006_order_order_img_order_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='cus_id',
            new_name='cus',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='submit_by',
            new_name='submit_emp',
        ),
        migrations.AlterField(
            model_name='order',
            name='create_date_time',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='submit_date_time',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
