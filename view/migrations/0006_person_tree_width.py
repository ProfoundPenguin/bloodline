# Generated by Django 4.2.7 on 2024-05-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view', '0005_renderedtree'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='tree_width',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]