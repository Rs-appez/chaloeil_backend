# Generated by Django 4.2.7 on 2023-11-26 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_alter_question_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_text',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='level_text',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(unique=True),
        ),
    ]