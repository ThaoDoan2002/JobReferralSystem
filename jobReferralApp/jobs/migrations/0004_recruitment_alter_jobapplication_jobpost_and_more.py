# Generated by Django 5.0.1 on 2024-02-02 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobapplication'),
        ('users', '0004_user_is_applicant_alter_employer_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('updated_date', models.DateField(auto_now=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255)),
                ('expirationDate', models.DateField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('sex', models.CharField(max_length=50)),
                ('workingForm', models.CharField(max_length=255)),
                ('areas', models.ManyToManyField(to='users.area')),
                ('carrers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='users.career')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='jobPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='jobs.recruitment'),
        ),
        migrations.DeleteModel(
            name='JobPost',
        ),
    ]