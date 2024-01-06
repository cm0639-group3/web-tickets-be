from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    def get_page_size(self, request):
        return super().get_page_size(request)
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
            # **{f'city_{index}': item for index, item in enumerate(data)}
        })

class ConditionalPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get('page_size', None)
        if page_size is not None:
            self.page_size = int(page_size)  # Set the pagination size
            return super().paginate_queryset(queryset, request, view)
        return None

    def get_paginated_response(self, data):
        if not self.page:
            return Response(data)  # If not paginating, return data directly

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
            # **{f'city_{index}': item for index, item in enumerate(data)}
        })
