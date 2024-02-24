from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('applicants', views.ApplicantViewSet, basename='applicants')
router.register('employers', views.EmployerViewSet, basename='employers')
router.register('skills', views.SkillViewSet, basename='skills')
router.register('areas', views.AreaViewSet, basename='areas')
router.register('careers', views.CareerViewSet, basename='careers')
router.register('comments',views.CommentViewSet, basename='comments')
router.register('ratings', views.RatingViewSet, basename='ratings')


urlpatterns = [
    path('', include(router.urls))
]