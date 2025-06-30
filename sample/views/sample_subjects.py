from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response

from sample.models import SampleSubject
from sample.functions.rest_framework import BaseAPIView


class SampleSubjectAPI(BaseAPIView):
    """
    API endpoint for retrieving subject information with caching, throttling, and filtering.
    
    This endpoint provides access to all subject data including subject names and codes.
    Results are cached for 15 minutes to improve performance. The endpoint supports
    searching, ordering, and pagination functionality.
    
    Throttling:
        - Anonymous users: 60 requests per hour
        - Authenticated users: Default DRF rate limits
    
    Filtering:
        Supports filtering by subject name or code through search parameter.
    
    Ordering:
        Supports ordering results through the ordering parameter.
    
    Pagination:
        Supports page-based pagination through query parameters.
    """

    def get(self, request):
        """
        Retrieve a list of all subjects with their names and codes.
        
        Parameters:
            request (Request): The HTTP request object containing query parameters
                - search (str, optional): Search term to filter subjects by name or code
                - ordering (str, optional): Field to order results by (e.g., 'name', '-name', 'subject_code')
                - page_size (int, optional): Number of results per page
                - page (int, optional): Page number to retrieve
        
        Returns:
            Response: A JSON response containing:
                - subjects (list): List of subject objects with the following fields:
                    - name (str): The subject name
                    - subject_code (str): The subject code
        
        Example Response:
            {
                "subjects": [
                    {
                        "name": "Mathematics",
                        "subject_code": "MATH"
                    },
                    {
                        "name": "English",
                        "subject_code": "ENG"
                    },
                    ...
                ]
            }
        """
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