# Generated by Django 5.1.4 on 2025-02-08 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_remove_answer_answer_text_answer_audio_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='audio_file',
            field=models.FileField(upload_to='audio_questions/'),
        ),
    ]
