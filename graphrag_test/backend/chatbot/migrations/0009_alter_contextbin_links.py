# Generated by Django 5.0.7 on 2024-08-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0008_remove_edge_source_edge_source_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contextbin',
            name='links',
            field=models.CharField(max_length=500),
        ),
    ]
