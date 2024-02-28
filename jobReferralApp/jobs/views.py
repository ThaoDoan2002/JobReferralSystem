from datetime import datetime

from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response

from jobs.models import RecruitmentPost, JobApplication
from users.models import Career
from jobs import serializers
from jobs import paginators
from django.utils import timezone
from rest_framework.decorators import action
from jobs import perms
from django_filters.rest_framework import DjangoFilterBackend
from jobs import filters
from django.db import connection
from debug_toolbar.panels import sql


# Create your views here.
class RecruitmentPostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = RecruitmentPost.objects.filter(active=True)
    serializer_class = serializers.RecruitmentPostSerializer
    pagination_class = paginators.RecruitmentPostPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RecruitmentPostFilter

    def get_queryset(self):
        queries = self.queryset

        for q in queries:
            if q.expirationDate <= timezone.now().date():
                q.active = False
                q.save()

        return queries

    def get_permissions(self):
        if self.action in ['create_post']:
            # Cho phép người dùng đã xác thực tạo mới (POST)
            return [perms.EmIsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Chỉ cho phép chủ sở hữu cập nhật (PUT, PATCH, DELETE)
            return [perms.EmOwnerAuthenticated()]
        elif self.action in ['search_posts', 'filter_posts']:
            return [perms.AppIsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False)
    def create_post(self, request):
        if request.data.get("career"):
            career = Career.objects.get(name__iexact=request.data.get("career"))
            p = RecruitmentPost.objects.create(employer=request.user.employer,
                                               title=request.data.get('title'),
                                               expirationDate=datetime.strptime(request.data.get('expirationDate'),
                                                                                "%Y-%m-%d").date(),
                                               experience=request.data.get('experience'),
                                               description=request.data.get('description'),
                                               quantity=request.data.get('quantity'),
                                               sex=request.data.get('sex'),
                                               workingForm=request.data.get('workingForm'),
                                               area=request.data.get('area'),
                                               wage=request.data.get('wage'),
                                               position=request.data.get('position'),
                                               career=career)
            queries = connection.queries
            num_queries = len(queries)
            return Response(serializers.RecruitmentPostSerializer(p).data, status=status.HTTP_201_CREATED)
            # return Response({"message": "API Response", "num_queries": num_queries}): 5
        return Response(serializers.RecruitmentPostSerializer(status=status.HTTP_400_BAD_REQUEST))

    @action(methods=['patch'], detail=True)
    def update_post(self, request, pk):
        post = self.get_object()
        if request.data.get("career"):
            career = Career.objects.get(name__iexact=request.data.get("career"))
            data_to_update = {
                'title': request.data.get('title', post.title),
                'expirationDate': request.data.get('expirationDate', post.expirationDate),
                'experience': request.data.get('experience', post.experience),
                'description': request.data.get('description', post.description),
                'quantity': request.data.get('quantity', post.quantity),
                'sex': request.data.get('sex', post.sex),
                'workingForm': request.data.get('workingForm', post.workingForm),
                'area': request.data.get('area', post.area),
                'wage': request.data.get('wage', post.wage),
                'position': request.data.get('position', post.position),
                'career': {
                    "id": career.id,
                    "name": career.name
                }
            }
            queries = connection.queries
            num_queries = len(queries)
            serializer = serializers.RecruitmentPostSerializer(post, data=data_to_update, partial=True)
        else:
            queries = connection.queries
            num_queries = len(queries)
            serializer = serializers.RecruitmentPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_data = serializer.data  # Get serialized data
            #return Response({"message": "API Response", "num_queries": num_queries}) 7,3
            return Response(updated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def search_posts(self, request):
        q = request.query_params.get("q")
        if q:
            careers = Career.objects.filter(name__icontains=q)

            posts = RecruitmentPost.objects.distinct().filter(
                Q(title__icontains=q) | Q(career__in=careers) | Q(workingForm__icontains=q) | Q(area__icontains=q)
            )
            if posts:
                page = self.paginate_queryset(posts)  # Phân trang dựa trên cấu hình trong pagination_class
                serializer = serializers.RecruitmentPostSerializer(page, many=True)
                queries = connection.queries
                num_queries = len(queries)
                #return Response({"message": "API Response", "num_queries": num_queries})4,5
                return self.get_paginated_response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter_posts(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queries = connection.queries
        num_queries = len(queries)
        #return Response({"message": "API Response", "num_queries": num_queries})3/5
        return Response(serializers.RecruitmentPostSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def apply_job(self, request, pk):
        post = self.get_object()
        applicant = request.user.applicant
        jobApp = JobApplication.objects.create(recruitment=post, applicant=applicant)
        queries = connection.queries
        num_queries = len(queries)
        #return Response({"message": "API Response", "num_queries": num_queries})5
        return Response(serializers.JobApplicationSerializer(jobApp).data, status=status.HTTP_201_CREATED)
