from rest_framework import serializers
from users.models import User, Applicant, Employer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_employer', 'is_applicant', 'phoneNumber', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Applicant
        fields = '__all__'

    def update(self, instance, validated_data):  # có thể sửa thông tin user bên trong employer instance
        user_data = validated_data.pop('user', {})  # Lấy dữ liệu của user từ validated_data
        user_instance = instance.user  # Lấy instance của user liên kết với Employer
        for attr, value in user_data.items():
            setattr(user_instance, attr, value)  # Cập nhật giá trị mới cho các trường của user
        user_instance.save()  # Lưu lại các thay đổi vào database
        return super().update(instance, validated_data)  # Gọi phương thức update của ModelSerializer

class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employer
        fields = '__all__'

    def update(self, instance, validated_data): #có thể sửa thông tin user bên trong employer instance
        user_data = validated_data.pop('user', {})  # Lấy dữ liệu của user từ validated_data
        user_instance = instance.user  # Lấy instance của user liên kết với Employer
        for attr, value in user_data.items():
            setattr(user_instance, attr, value)  # Cập nhật giá trị mới cho các trường của user
        user_instance.save()  # Lưu lại các thay đổi vào database
        return super().update(instance, validated_data)  # Gọi phương thức update của ModelSerializer