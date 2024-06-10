# Generated by Django 5.0.6 on 2024-06-05 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0036_rename_orignial_amount_order_original_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='original_amount',
        ),
        migrations.AddField(
            model_name='order',
            name='order_message',
            field=models.JSONField(default=0),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='discount',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='types',
            field=models.JSONField(default=list),
        ),
    ]
