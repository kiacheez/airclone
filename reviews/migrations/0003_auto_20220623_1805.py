# Generated by Django 2.2.5 on 2022-06-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_review_id_alter_review_room_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
