# Generated by Django 3.0.6 on 2021-07-23 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogtbl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacttbl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=200, null=True)),
                ('sender_email', models.EmailField(max_length=254)),
                ('sender_message', models.TextField()),
            ],
        ),
    ]
