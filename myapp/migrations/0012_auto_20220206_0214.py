# Generated by Django 3.0.4 on 2022-02-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_jobs_pool'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs_pool',
            name='Released_Date',
            field=models.CharField(default='none', max_length=40),
        ),
    ]