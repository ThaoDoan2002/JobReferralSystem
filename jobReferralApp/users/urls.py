from django.urls import path, include
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename='users')
router.register('applicants', views.ApplicantViewSet, basename='applicants')

urlpatterns = [
    path('', include(router.urls))
]