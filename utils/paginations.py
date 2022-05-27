from rest_framework.pagination import PageNumberPagination

class PazeSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size' # no of results
    max_page_size = 50
    page_query_param = 'page' # page no