from rest_framework.pagination import PageNumberPagination

class RecruitmentPostPaginator(PageNumberPagination):
    page_size = 20