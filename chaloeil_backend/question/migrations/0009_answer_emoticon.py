# Generated by Django 5.0.6 on 2024-07-07 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_alter_question_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='emoticon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
