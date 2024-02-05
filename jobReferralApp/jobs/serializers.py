from jobs.models import Recruitment
from rest_framework import serializers


class RecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment
        fields = '__all__'