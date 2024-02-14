from jobs.models import RecruitmentPost
from rest_framework import serializers


class RecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentPost
        fields = '__all__'