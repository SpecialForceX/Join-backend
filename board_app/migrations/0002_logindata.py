# Generated by Django 5.1.7 on 2025-03-10 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
