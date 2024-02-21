# Generated by Django 4.2.10 on 2024-02-21 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_career_applicant_applicant_career_and_more'),
        ('jobs', '0006_alter_recruitmentpost_expirationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentpost',
            name='employer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.employer'),
        ),
    ]