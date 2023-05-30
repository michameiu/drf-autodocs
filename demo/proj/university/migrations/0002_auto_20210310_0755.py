# Generated by Django 3.1.4 on 2021-03-10 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lecturer',
            name='task_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]