from jobs.models import RecruitmentPost
from users.serializers import EmployerSerializer
from rest_framework import serializers
from jobs.models import RecruitmentPost
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









