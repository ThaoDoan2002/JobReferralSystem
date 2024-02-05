from django.urls import path,include
from rest_framework import routers
from jobs import views

router = routers.DefaultRouter()
router.register('recruitments', views.RecruitmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
