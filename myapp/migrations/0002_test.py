# Generated by Django 3.0.4 on 2021-12-16 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Skills', models.CharField(max_length=100)),
                ('Amount', models.SmallIntegerField(default=0)),
            ],
        ),
    ]