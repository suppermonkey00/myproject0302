# Generated by Django 3.2.3 on 2021-06-13 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20210611_0146'),
        ('order', '0004_order_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='variant',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.variants'),
        ),
    ]
