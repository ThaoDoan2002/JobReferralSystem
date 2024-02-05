# Generated by Django 5.0.1 on 2024-02-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_remove_recruitment_carrers'),
        ('users', '0007_alter_career_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='career',
            field=models.CharField(choices=[('Kinh doanh / Bán hàng', 'Kinh doanh / Bán hàng'), ('Biên / Phiên dịch', 'Biên / Phiên dịch'), ('Báo chí / Truyền hình', 'Báo chí / Truyền hình'), ('Bưu chính - Viễn thông', 'Bưu chính - Viễn thông'), ('Bảo hiểm', 'Bảo hiểm'), ('Bất động sản', 'Bất động sản'), ('Chứng khoán / Vàng / Ngoại tệ', 'Chứng khoán / Vàng / Ngoại tệ'), ('Công nghệ cao', 'Công nghệ cao'), ('Cơ khí / Chế tạo / Tự động hóa', 'Cơ khí / Chế tạo / Tự động hóa'), ('Du lịch', 'Du lịch'), ('Ngành nghề', 'Ngành nghề')], default='Ngành nghề', max_length=50),
        ),
        migrations.DeleteModel(
            name='Career',
        ),
    ]