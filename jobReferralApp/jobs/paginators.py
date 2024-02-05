from rest_framework.pagination import PageNumberPagination

class RecruitmentPaginator(PageNumberPagination):
    page_size = 2