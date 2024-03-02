import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import viewsets, generics, permissions, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Applicant, Employer, Skill, Area, Career, Comment, Like, Rating
from users import serializers
from jobs.serializers import RecruitmentPostSerializer
from users import perms
from users import filters
from jobs.models import RecruitmentPost

from users.serializers import PasswordResetSerializer


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False)
    def current_user(self, request):
        # cac thong tin sau khi da chung thuc nam trong request.user
        if request.user.is_applicant:
            return Response(serializers.ApplicantSerializer(request.user.applicant, context={'request': request}).data)
        elif request.user.is_employer:
            return Response(serializers.EmployerSerializer(request.user.employer, context={'request': request}).data)
        else:
            return Response(serializers.UserSerializer(request.user).data, status=status.HTTP_200_OK)



class ApplicantViewSet(viewsets.ViewSet,generics.RetrieveAPIView, generics.ListAPIView):
    queryset = Applicant.objects.all()
    serializer_class = serializers.ApplicantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ApplicantFilter

    def get_permissions(self):
        if self.action in ['update_applicant']:
            return [perms.AppOwnerAuthenticated()]
        elif self.action in ['search_applicant', 'filter_applicant']:
            return [perms.EmIsAuthenticated()]
        elif self.action.__eq__('suggest_Job'):
            return [perms.AppIsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False)
    def search_applicant(self, request):
        q = request.query_params.get("q")

        if q:
            skills = Skill.objects.filter(name__icontains=q)
            areas = Area.objects.filter(name__icontains=q)
            careers = Career.objects.filter(name__icontains=q)

            applicants = Applicant.objects.distinct().filter(
                Q(skills__in=skills) | Q(areas__in=areas) | Q(career__in=careers))

            if applicants:
                return Response(serializers.ApplicantSerializer(applicants, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def filter_applicant(self, request):
        # Lấy queryset đã được lọc
        queryset = self.filter_queryset(self.get_queryset())
        return Response(serializers.ApplicantSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def update_applicant(self, request, pk):
        applicant = self.get_object()
        if request.data.get("career"):
            career = Career.objects.get(name__iexact=request.data.get("career"))
            data_to_update = {
                'position': request.data.get('position', applicant.position),
                'experience': request.data.get('experience', applicant.experience),
                'wage': request.data.get('wage', applicant.wage),
                'cv': request.data.get('cv', applicant.cv),
                'career': {
                    "id": career.id,
                    "name": career.name
                }
            }
            if request.data.get('skills'):
                skills_data = request.data.get('skills')

                if skills_data:
                    # Xóa tất cả các kỹ năng hiện có của applicant
                    applicant.skills.clear()

                    # Lặp qua danh sách các kỹ năng mới và thêm chúng vào applicant
                    for skill_name in skills_data:
                        # Kiểm tra xem kỹ năng đã tồn tại trong DB chưa
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        # Thêm kỹ năng vào danh sách kỹ năng của applicant
                        applicant.skills.add(skill)
            if request.data.get('areas'):
                areas_data = request.data.get('areas')

                if areas_data:
                    # Xóa tất cả các kỹ năng hiện có của applicant
                    applicant.areas.clear()

                    # Lặp qua danh sách các kỹ năng mới và thêm chúng vào applicant
                    for area_name in areas_data:
                        # Kiểm tra xem kỹ năng đã tồn tại trong DB chưa
                        area, created = Area.objects.get_or_create(name=area_name)
                        # Thêm kỹ năng vào danh sách kỹ năng của applicant
                        applicant.areas.add(area)
            serializer = serializers.ApplicantSerializer(applicant, data=data_to_update, partial=True)
        elif request.data.get("career") is None:
            data_to_update = {
                'position': request.data.get('position', applicant.position),
                'experience': request.data.get('experience', applicant.experience),
                'wage': request.data.get('wage', applicant.wage),
                'cv': request.data.get('cv', applicant.cv),
            }
            if request.data.get('skills'):
                skills_data = request.data.get('skills')

                if skills_data:
                    # Xóa tất cả các kỹ năng hiện có của applicant
                    applicant.skills.clear()

                    # Lặp qua danh sách các kỹ năng mới và thêm chúng vào applicant
                    for skill_name in skills_data:
                        # Kiểm tra xem kỹ năng đã tồn tại trong DB chưa
                        skill, created = Skill.objects.get_or_create(name=skill_name)
                        # Thêm kỹ năng vào danh sách kỹ năng của applicant
                        applicant.skills.add(skill)
            if request.data.get('areas'):
                areas_data = request.data.get('areas')

                if areas_data:
                    # Xóa tất cả các kỹ năng hiện có của applicant
                    applicant.areas.clear()

                    # Lặp qua danh sách các kỹ năng mới và thêm chúng vào applicant
                    for area_name in areas_data:
                        # Kiểm tra xem kỹ năng đã tồn tại trong DB chưa
                        area, created = Area.objects.get_or_create(name=area_name)
                        # Thêm kỹ năng vào danh sách kỹ năng của applicant
                        applicant.areas.add(area)
            serializer = serializers.ApplicantSerializer(applicant, data=data_to_update, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_data = serializer.data  # Get serialized data
            return Response(updated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def suggest_Job(self, request):
        applicant = request.user.applicant

        applicant_areas = applicant.areas.values_list('name', flat=True)
        posts = RecruitmentPost.objects.filter(experience__icontains=applicant.experience,
                                               sex__icontains=applicant.user.sex,
                                               area__in=applicant_areas,
                                               wage__icontains=applicant.wage,
                                               position__icontains=applicant.position,
                                               career=applicant.career,
                                               workingForm__icontains=applicant.workingForm)
        return Response(RecruitmentPostSerializer(posts, many=True).data, status=status.HTTP_200_OK)


class EmployerViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Employer.objects.all()
    serializer_class = serializers.EmployerSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [perms.EmOwnerAuthenticated()]
        elif self.action in ('search_employer', 'like', 'add_comment','add_rating'):
            return [perms.AppIsAuthenticated()]
        elif self.action.__eq__('get_posts'):
            return [perms.EmIsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True)
    def get_employer(self,request,pk):
        em = self.get_object()
        return Response(serializers.EmployerDetailSerializer(em,context={"request": request}).data, status=status.HTTP_200_OK, )

    @action(methods=['get'], detail=False)
    def search_employer(self, request):
        q = request.query_params.get("q")
        if q:
            employers = Employer.objects.filter(companyName__icontains=q)
            if employers:
                return Response(serializers.EmployerSerializer(employers, many=True).data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def get_posts(self,request,pk):
        posts = RecruitmentPost.objects.filter(employer=self.get_object())
        return Response(serializers.RecruitmentPostSerializer(posts, many=True).data,status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='comments')
    def add_comment(self, request, pk):
        c = Comment.objects.create(applicant=request.user.applicant, employer=self.get_object(),
                                   content=request.data.get('content'))
        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(applicant=request.user.applicant, employer=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        return Response(serializers.EmployerDetailSerializer(self.get_object(), context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rating')
    def add_rating(self, request, pk):
        rating = Rating.objects.create(applicant=request.user.applicant, employer=self.get_object(),
                                       rate=request.data.get('rate'))
        return Response(serializers.RatingSerializer(rating).data,status=status.HTTP_201_CREATED)


class RatingViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
        queryset = Rating.objects.all()
        serializer_class = serializers.RatingSerializer
        permission_classes = [perms.AppOwnerCmtAuthenticated]


class CommentViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.AppOwnerCmtAuthenticated]


class SkillViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = serializers.SkillSerilizer


class AreaViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Area.objects.all()
    serializer_class = serializers.AreaSerilizer


class CareerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Career.objects.all()
    serializer_class = serializers.CareerSerilizer


class PasswordResetViewset(viewsets.ViewSet):
    serializer_class = PasswordResetSerializer

    @action(methods=['post'], detail=False)
    def sendmail(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Generate token
            token = default_token_generator.make_token(user)

            # Construct reset link
            # Tạo mã xác nhận ngẫu nhiên
            confirmation_code = ''.join(random.choices('0123456789', k=6))
            # Lưu mã xác nhận vào cơ sở dữ liệu hoặc cache
            # Ở đây ta lưu vào session
            request.session['confirmation_code'] = confirmation_code
            request.session['email'] = email

            send_mail(
                'Xác nhận đổi mật khẩu',
                f'Mã xác nhận của bạn là: {confirmation_code}',
                'your@email.com',
                [email],
                fail_silently=False,
            )

            return Response({"success": "Password reset link sent successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def confirm_code(self, request):
        code = request.data.get('code')

        if 'confirmation_code' in request.session and 'email' in request.session:
            if code == request.session['confirmation_code']:
                # Xác nhận thành công
                return Response({'success': 'Mã xác nhận hợp lệ'}, status=status.HTTP_200_OK)

        return Response({'error': 'Mã xác nhận không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'error': 'Mật khẩu không khớp'}, status=status.HTTP_400_BAD_REQUEST)

        if 'email' in request.session:
            # Thay đổi mật khẩu
            user = User.objects.get(email=request.session['email'])
            user.password = make_password(new_password)
            user.save()

            # Xóa session sau khi thay đổi mật khẩu thành công
            del request.session['email']

            return Response({'success': 'Thay đổi mật khẩu thành công'}, status=status.HTTP_200_OK)

        return Response({'error': 'Mã xác nhận chưa được xác thực'}, status=status.HTTP_400_BAD_REQUEST)