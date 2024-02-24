from jobs.models import RecruitmentPost
from users.serializers import EmployerSerializer, ApplicantSerializer
from rest_framework import serializers
from jobs.models import RecruitmentPost, JobApplication
from users.models import Career


class CareerSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'


class RecruitmentPostSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()
    career = CareerSerialzier()
    class Meta:
        model = RecruitmentPost
        fields = '__all__'

    def update(self, instance, validated_data):
        career_data = validated_data.pop('career', None)
        if career_data:
            career_instance = Career.objects.get(**career_data)
            instance.career = career_instance

        return super().update(instance, validated_data)


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


