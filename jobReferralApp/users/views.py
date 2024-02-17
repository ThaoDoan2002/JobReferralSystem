from rest_framework import viewsets, generics, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User,Applicant, Employer
from users import serializers
from users import perms


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    #không tách current-user vì khi chỉ lấy mỗi user information, thì khi cần tới thông tin của employer hay applicant phải tốn thêm 1 query truy xuất, nếu thêm field method cho UserSerializer, thì sẽ rối 2 role


class ApplicantViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = serializers.ApplicantSerializer

    def get_permissions(self):
        if self.action.__eq__('current_applicant'):
            return [permissions.IsAuthenticated()]
        return [perms.OwnerAuthenticated()]

    @action(methods=['get'], url_name='current_applicant', detail=False)
    def current_applicant(self, request):
        # cac thong tin sau khi da chung thuc nam trong request.user
        return Response(serializers.ApplicantSerializer(request.user.applicant).data)




class EmployerViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Employer.objects.all()
    serializer_class = serializers.EmployerSerializer

    def get_permissions(self):
        if self.action.__eq__('current_employer'):
            return [permissions.IsAuthenticated()]
        return [perms.OwnerAuthenticated()]

    @action(methods=['get'], url_name='current_employer', detail=False)
    def current_employer(self, request):
        # cac thong tin sau khi da chung thuc nam trong request.user
        return Response(serializers.EmployerSerializer(request.user.employer).data)





