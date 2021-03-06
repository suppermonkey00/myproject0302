# Generated by Django 3.2.3 on 2021-06-07 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_comment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='minamount',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
