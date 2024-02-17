from jobs.models import RecruitmentPost
from users.serializers import EmployerSerializer
from rest_framework import serializers
from jobs.models import RecruitmentPost


class RecruitmentPostSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer()

    class Meta:
        model = RecruitmentPost
        fields = '__all__'








