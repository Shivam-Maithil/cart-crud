# Generated by Django 4.1.1 on 2022-10-02 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kart', '0002_alter_product_under_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='under_category',
            field=models.ManyToManyField(blank=True, to='kart.category'),
        ),
    ]