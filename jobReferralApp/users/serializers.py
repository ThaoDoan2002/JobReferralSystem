from rest_framework import serializers
from users.models import User, Applicant, Employer, Skill, Area, Career, Comment, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_employer', 'is_applicant',
                  'phoneNumber', 'avatar', 'is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class SkillSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class AreaSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CareerSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    skills = SkillSerilizer(many=True)
    areas = AreaSerilizer(many=True)
    career = CareerSerilizer()

    class Meta:
        model = Applicant
        fields = '__all__'

    # Khi update applicant đồng thời thay đổi thông tin cơ bản trong user
    def update(self, instance, validated_data):
        # Cập nhật thông tin của user nếu có
        user_data = validated_data.pop('user', {})
        user_instance = instance.user
        for attr, value in user_data.items():
            setattr(user_instance, attr, value)
        user_instance.save()
        # update career
        career_data = validated_data.pop('career', None)
        if career_data:
            career_instance = Career.objects.get(**career_data)
            instance.career = career_instance
        return super().update(instance, validated_data)


class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employer
        fields = ['user', 'companyName','position','information','address','mediaLink','companySize']

    def update(self, instance, validated_data):  # có thể sửa thông tin user bên trong employer instance
        user_data = validated_data.pop('user', {})  # Lấy dữ liệu của user từ validated_data
        user_instance = instance.user  # Lấy instance của user liên kết với Employer
        for attr, value in user_data.items():
            setattr(user_instance, attr, value)  # Cập nhật giá trị mới cho các trường của user
        user_instance.save()  # Lưu lại các thay đổi vào database
        return super().update(instance, validated_data)


class EmployerDetailSerializer(EmployerSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, employer):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return employer.like_set.filter(active=True).exists()

    class Meta:
        model = EmployerSerializer.Meta.model
        fields = EmployerSerializer.Meta.fields + ['liked']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

