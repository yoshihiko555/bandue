from rest_framework.pagination import (
    PageNumberPagination,
)
from rest_framework.exceptions import NotFound

import logging
logger = logging.getLogger(__name__)


class StandardResultSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50


class StandardListResultSetPagination(PageNumberPagination):
    """
    リストをページネーションで返したい場合、このクラスを使用。
    """

    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, list, request, view=None):

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(list, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return self.page
