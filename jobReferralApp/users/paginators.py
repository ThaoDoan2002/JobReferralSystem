from rest_framework.pagination import PageNumberPagination

class ApplicantPaginator(PageNumberPagination):
    page_size = 2
