"""DRF Pagination Settings for Hypoxic Service"""
from collections import OrderedDict

from rest_framework_json_api import pagination as json_api_pagination


class PageNumberPagination(json_api_pagination.PageNumberPagination):
    """
    Overrides the page_query_param and page_size_query_param values
    with page[number] and page[size] respectively.

    Copied from authorization-service

    For example:
        http://api.example.org/accounts/?page[number]=4
        http://api.example.org/accounts/?page[number]=4&page[size]=100
    """
    page_query_param = 'page[number]'
    page_size_query_param = 'page[size]'

    def get_paginated_response(self, data):
        """
        Add page[number] and page[size] to Response meta pagination.
        """
        response = super().get_paginated_response(data)
        response.data['meta']['pagination'] = OrderedDict(
            [
                (self.page_query_param, self.page.number),
                (self.page_size_query_param, self.page.paginator.per_page),
                ('pages', self.page.paginator.num_pages),
                ('count', self.page.paginator.count),
            ]
        )
        return response
