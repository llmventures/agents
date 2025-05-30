# Generated by Django 5.0.7 on 2024-08-08 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
                ('input_format', models.CharField(max_length=30)),
                ('output_format', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
                ('input_format', models.CharField(max_length=30)),
                ('output_format', models.CharField(max_length=30)),
                ('agents', models.ManyToManyField(to='chatbot.agent')),
            ],
        ),
    ]
