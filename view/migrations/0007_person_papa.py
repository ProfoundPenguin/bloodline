# Generated by Django 4.2.7 on 2024-05-09 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0006_person_tree_width'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='papa',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
