# Generated by Django 4.1.7 on 2023-06-23 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('LittleLemonDRF', '0002_remove_cart_price_remove_cart_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_crew', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LittleLemonDRF.order'),
        ),
    ]
