# Generated by Django 3.0.4 on 2021-12-18 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20211218_1505'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='position_sk_sum',
            new_name='position_sk_post_sum',
        ),
    ]