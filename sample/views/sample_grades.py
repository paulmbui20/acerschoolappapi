from django.core.cache import cache
from rest_framework import status

from rest_framework.response import Response


from sample.models import SampleGrade
from sample.functions.rest_framework import BaseAPIView


class SampleGradeAPI(BaseAPIView):
    def get(self, request):
        cache_key = f"grades_{request.META['QUERY_STRING']}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        overall_grades = SampleGrade.objects.all()

        page_size = request.query_params.get('page_size', None)
        page = request.query_params.get('page', None)

        if page_size and page:
            try:
                page_size = int(page_size)
                page = int(page)

                overall_start = (page - 1) * page_size
                overall_end = overall_start + page_size
                overall_grades = overall_grades[overall_start:overall_end]
            except (ValueError, TypeError):
                pass

        response_data = {
            'overall_grades': list(overall_grades.values(
                'grade_letter', 'min_score', 'max_score', 'points', 'comment'
            )),
        }

        cache.set(cache_key, response_data, timeout=60 * 15)

        return Response(response_data, status=status.HTTP_200_OK)