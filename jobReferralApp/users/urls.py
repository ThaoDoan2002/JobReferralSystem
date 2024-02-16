from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('applicants', views.ApplicantViewSet, basename='applicants')
router.register('employers', views.EmployerViewSet, basename='employers')

urlpatterns = [
    path('', include(router.urls))
]