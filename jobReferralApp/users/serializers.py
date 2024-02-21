from rest_framework import serializers
from users.models import User, Applicant, Employer, Skill, Area, Career
class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, user):
        if user.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % user.image.name)
            return '/static/%s' % user.image.name

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'is_employer', 'is_applicant', 'phoneNumber', 'avatar','image']
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
    cv = serializers.SerializerMethodField(source='cv')

    def get_cv(self, applicant):
        if applicant.cv:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % applicant.cv.name)
            return '/static/%s' % applicant.cv.name
    class Meta:
        model = Applicant
        fields = '__all__'

#Khi update applicant đồng thời thay đổi thông tin cơ bản trong user
    def update(self, instance, validated_data):
        # Cập nhật thông tin của user nếu có
        user_data = validated_data.pop('user', {})
        user_instance = instance.user
        for attr, value in user_data.items():
            setattr(user_instance, attr, value)
        user_instance.save()

        # Cập nhật thông tin của Employer
        instance.position = validated_data.get("position", instance.position)
        instance.wage = validated_data.get("wage", instance.wage)
        instance.experience = validated_data.get("experience", instance.experience)
        # instance.career = validated_data.get('career', instance.career)
        # Cập nhật các trường khác tùy theo yêu cầu

        # Lưu lại instance Employer đã cập nhật
        instance.save()

        # Lấy ra danh sách kỹ năng mới từ validated_data
        skills_data = validated_data.pop("skills", [])
        # Xóa hết các kỹ năng cũ của Employer
        instance.skills.clear()
        # Thêm kỹ năng mới
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(**skill_data)
            instance.skills.add(skill)

        # Lấy ra danh sách khu vực mới từ validated_data
        areas_data = validated_data.pop("areas", [])
        # Xóa hết các khu vực cũ của Employer
        instance.areas.clear()
        # Thêm khu vực mới
        for area_data in areas_data:
            area, created = Area.objects.get_or_create(**area_data)
            instance.areas.add(area)

        career_data = validated_data.pop('career', None)
        if career_data:
            career_id = career_data.get('id', None)
            career_name = career_data.get('name', None)

            if career_id is not None and career_name is not None:
                raise serializers.ValidationError("Chỉ cung cấp `id` hoặc `name`, không cùng lúc.")

            if career_id is not None:
                try:
                    career = Career.objects.get(id=career_id)
                    instance.career = career
                except Career.DoesNotExist:
                    raise serializers.ValidationError("Career with id={} does not exist.".format(career_id))
            elif career_name is not None:
                try:
                    career = Career.objects.get(name=career_name)
                    instance.career = career
                except Career.DoesNotExist:
                    raise serializers.ValidationError("Career with name={} does not exist.".format(career_name))

        instance.save()
        return instance

        instance.save()

        return super().update(instance, validated_data)

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



