from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response

from jobs.models import RecruitmentPost
from jobs import serializers
from jobs import paginators
from django.utils import timezone
from rest_framework.decorators import action
from jobs import perms




# Create your views here.
class RecruitmentPostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = RecruitmentPost.objects.filter(active=True)
    serializer_class = serializers.RecruitmentPostSerializer
    pagination_class = paginators.RecruitmentPostPaginator

    def get_queryset(self):
        queries = self.queryset

        for q in queries:
            if q.expirationDate <= timezone.now().date():
                q.active = False
                q.save()

        return queries

    def get_permissions(self):
        if self.action.__eq__('create_post'):
            # Cho phép người dùng đã xác thực tạo mới (POST)
            return [perms.EmIsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Chỉ cho phép chủ sở hữu cập nhật (PUT, PATCH, DELETE)
            return [perms.OwnerAuthenticated()]
        else:
            # Mặc định, cho phép tất cả các hành động khác
            return [permissions.AllowAny()]

    @action(methods=['post'], detail=False)
    def create_post(self, request):
        p = RecruitmentPost.objects.create(employer=request.user.employer, title=request.data.get('title'),expirationDate= datetime.strptime(request.data.get('expirationDate'), "%Y-%m-%d").date())
        return Response(serializers.RecruitmentPostSerializer(p).data, status=status.HTTP_201_CREATED)



