# Generated by Django 4.2.8 on 2024-03-01 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("task_instance", "0009_alter_taskinstance_duration_worked"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="taskinstance",
            options={
                "permissions": [
                    ("start_task_instance", "Can start a task"),
                    ("stop_task_instance", "Can stop a task"),
                ]
            },
        ),
    ]
