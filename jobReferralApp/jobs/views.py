from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import RecruitmentPost
from jobs import serializers
from jobs import  paginators

# Create your views here.
class RecruitmentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = RecruitmentPost.objects.all()
    serializer_class = serializers.RecruitmentSerializer
    pagination_class = paginators.RecruitmentPaginator
