

from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response

from .models import RecruitmentPost
from jobs import serializers
from jobs import paginators
from django.utils import timezone
from rest_framework.decorators import action
from datetime import datetime
from jobs import perms


# Create your views here.
class RecruitmentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = RecruitmentPost.objects.filter(active=True)
    serializer_class = serializers.RecruitmentSerializer
    pagination_class = paginators.RecruitmentPaginator

    def get_queryset(self):
        queries = self.queryset

        for q in queries:
            if q.expirationDate <= timezone.now().date():
                q.active = False
                q.save()

        return queries

    def get_permissions(self):
        if self.action.__eq__('add_recruitmentPost'):
            return [permissions.IsAuthenticated()]
        elif self.action.__eq__('update_recruitmentPost') | self.action.__eq__('delete_recruitmentPost'):
            return [perms.OwnerAuthenticated()]

        return [permissions.AllowAny()]


    @action(methods=['post'],detail=False, url_path='add_recruitmentPost')
    def add_recruitmentPost(self, request):
        if request.user.is_employer:
            r = RecruitmentPost.objects.create(employer=request.user.employer,
                                               title=request.data.get('title'),experience=request.data.get('experience'),expirationDate= datetime.strptime(request.data.get('expirationDate'), "%Y-%m-%d").date())
            return Response(serializers.RecruitmentSerializer(r).data,status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True,url_path='update_recruitmentPost')
    def update_recruitmentPost(self,request,pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['delete'], detail=True)
    def delete_recruitmentPost(self,request,pk):
            r = self.get_object()
            r.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

