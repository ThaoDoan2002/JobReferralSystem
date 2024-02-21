from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, generics, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from users.models import User,Applicant, Employer, Skill, Area, Career
from users import serializers
from users import perms
from users import filters
from users import paginators



# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('curent_user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


    @action(methods=['get'], detail=False)
    def current_user(self, request):
        # cac thong tin sau khi da chung thuc nam trong request.user
        if request.user.is_applicant:
            return Response(serializers.ApplicantSerializer(request.user.applicant, context={'request': request}).data)
        elif request.user.is_employer:
            return Response(serializers.EmployerSerializer(request.user.employer, context={'request': request}).data)

    #không tách current-user vì khi chỉ lấy mỗi user information, thì khi cần tới thông tin của employer hay applicant phải tốn thêm 1 query truy xuất, nếu thêm field method cho UserSerializer, thì sẽ rối 2 role


class ApplicantViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.ListAPIView):
    queryset = Applicant.objects.all()
    serializer_class = serializers.ApplicantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ApplicantFilter
    pagination_class = paginators.ApplicantPaginator

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [perms.AppOwnerAuthenticated()]
        return  [permissions.AllowAny()]
        # if self.action.__eq__('get'):
        #     return [perms.EmIsAuthenticated()]

    # @action(methods=['get'], detail=False)
    # def search_applicant(self,request):
    #     q = self.filter_queryset(self.get_queryset())
    #     return Response(serializers.ApplicantSerializer(q,many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def searchApplicant(self, request):
        q = self.request.query_params.get("q")

        if q:
            skills = Skill.objects.filter(name__icontains=q)
            areas = Area.objects.filter(name__icontains=q)
            careers = Career.objects.filter(name__icontains=q)

            applicants = Applicant.objects.distinct().filter(Q(skills__in=skills)|Q(areas__in=areas)|Q(career__in =careers))

            if applicants:
                page = self.paginate_queryset(applicants)  # Phân trang dựa trên cấu hình trong pagination_class
                serializer = serializers.ApplicantSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)





class EmployerViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Employer.objects.all()
    serializer_class = serializers.EmployerSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [perms.EmOwnerAuthenticated()]
        else:
            return [permissions.AllowAny()]


class SkillViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = serializers.SkillSerilizer

class AreaViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerilizer

class CareerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = serializers.CareerSerilizer











