# Generated by Django 5.0.7 on 2024-08-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0002_remove_agent_id_remove_crew_id_alter_agent_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crew',
            old_name='role',
            new_name='task',
        ),
        migrations.AddField(
            model_name='agent',
            name='backstory',
            field=models.CharField(default=[], max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agent',
            name='goal',
            field=models.CharField(default=[], max_length=100),
            preserve_default=False,
        ),
    ]
