# Generated by Django 4.0.4 on 2022-06-24 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20220623_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
