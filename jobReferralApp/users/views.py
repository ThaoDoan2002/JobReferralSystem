from rest_framework import viewsets, generics, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users import serializers


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]


    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current_user', detail=False)
    def current_user(self, request):
        #cac thong tin sau khi da chung thuc nam trong request.user
        return Response(serializers.UserSerializer(request.user).data)

