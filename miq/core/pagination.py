from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import serialize_context_pagination


class MiqPageNumberPagination(PageNumberPagination):
    page_size = 16

    def get_paginated_response(self, data):
        page = self.page
        context = {
            'is_paginated': page.has_other_pages(),
            'page_obj': page,
            'paginator': page.paginator
        }

        _r = serialize_context_pagination(self.request, context)
        _r['has_next_url'] = self.get_next_link()
        _r['has_previous_url'] = self.get_previous_link()
        _r['results'] = data
        _r['is_drf'] = True

        return Response(_r)
