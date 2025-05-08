# pagination.py
from rest_framework.pagination import PageNumberPagination

class PageNumberPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum page size limit
