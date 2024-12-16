# Generated by Django 3.0.4 on 2021-12-17 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='data_analyst_sk_sum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(max_length=100)),
                ('Amount', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='network_engineer_sk_sum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(max_length=100)),
                ('Amount', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='software_engineer_sk_sum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(max_length=100)),
                ('Amount', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Web_developer_sk_sum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(max_length=100)),
                ('Amount', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.RenameModel(
            old_name='test',
            new_name='cloud_architect_sk_sum',
        ),
    ]