from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from sample.models import SampleSubject
from sample.functions.rest_framework import BaseAPIView


class SampleSubjectAPI(BaseAPIView):
    """
    API endpoint for sample subjects with caching, throttling, and filtering
    """

    def get(self, request):
        cache_key = f"subjects_{request.META['QUERY_STRING']}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        subjects = SampleSubject.objects.all()

        search_query = request.query_params.get('search', None)
        if search_query:
            subjects = subjects.filter(name__icontains=search_query) | \
                       subjects.filter(subject_code__icontains=search_query)

        ordering = request.query_params.get('ordering', None)
        if ordering:
            subjects = subjects.order_by(ordering)

        page_size = request.query_params.get('page_size', None)
        page = request.query_params.get('page', None)

        if page_size and page:
            try:
                page_size = int(page_size)
                page = int(page)
                start = (page - 1) * page_size
                end = start + page_size
                subjects = subjects[start:end]
            except (ValueError, TypeError):
                pass

        response_data = {
            'subjects': list(subjects.values('name', 'subject_code'))
        }

        cache.set(cache_key, response_data, timeout=60 * 15)

        return Response(response_data, status=status.HTTP_200_OK)