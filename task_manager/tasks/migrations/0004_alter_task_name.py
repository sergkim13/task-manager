# Generated by Django 4.1.7 on 2023-04-25 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='name'),
        ),
    ]