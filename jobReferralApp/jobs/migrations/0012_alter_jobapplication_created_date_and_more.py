# Generated by Django 4.2.10 on 2024-02-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_alter_like_unique_together_remove_like_lesson_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='recruitmentpost',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='recruitmentpost',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
