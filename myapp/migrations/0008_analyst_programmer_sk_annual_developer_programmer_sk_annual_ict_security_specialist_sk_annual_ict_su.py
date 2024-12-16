# Generated by Django 3.0.4 on 2022-01-16 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20211218_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='analyst_programmer_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='developer_programmer_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ict_security_specialist_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ict_support_engineer_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='network_administrator_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='network_analyst_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='software_tester_sk_annual',
            fields=[
                ('month', models.CharField(default='none', max_length=100, primary_key=True, serialize=False)),
                ('dataframe', models.CharField(default='none', max_length=500)),
                ('post', models.SmallIntegerField(default=0)),
            ],
        ),
    ]