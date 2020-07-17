from rest_framework.pagination import PageNumberPagination

class ModifiablePagination (PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'


class LargeModifiablePagination (PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_size_query_param = 'page_size'
