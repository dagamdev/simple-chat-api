# Generated by Django 4.2.5 on 2023-10-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_customuser_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_url',
            field=models.URLField(max_length=400, null=True),
        ),
    ]
