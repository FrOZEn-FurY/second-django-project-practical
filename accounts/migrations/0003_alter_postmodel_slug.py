# Generated by Django 4.2.3 on 2023-07-20 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_postmodel_slug_alter_postmodel_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='slug',
            field=models.SlugField(default='Slug', max_length=100),
        ),
    ]
