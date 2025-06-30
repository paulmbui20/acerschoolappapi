from django.core.cache import cache
from rest_framework import status

from rest_framework.response import Response


from sample.models import SampleGrade
from sample.functions.rest_framework import BaseAPIView


class SampleGradeAPI(BaseAPIView):
    """
    API endpoint for retrieving grade information with caching, throttling, and filtering.
    
    This endpoint provides access to all grade data including grade letters, score ranges,
    points, and comments. Results are cached for 15 minutes to improve performance.
    
    Throttling:
        - Anonymous users: 60 requests per hour
        - Authenticated users: Default DRF rate limits
    
    Pagination:
        Supports page-based pagination through query parameters.
    """
    
    def get(self, request):
        """
        Retrieve a list of all grades with their score ranges, points, and comments.
        
        Parameters:
            request (Request): The HTTP request object containing query parameters
                - page_size (int, optional): Number of results per page
                - page (int, optional): Page number to retrieve
        
        Returns:
            Response: A JSON response containing:
                - overall_grades (list): List of grade objects with the following fields:
                    - grade_letter (str): The letter grade (e.g., 'A', 'B+', 'C')
                    - min_score (float): Minimum score required for this grade
                    - max_score (float): Maximum score for this grade
                    - points (int): Points awarded for this grade
                    - comment (str): Descriptive comment for this grade
        
        Example Response:
            {
                "overall_grades": [
                    {
                        "grade_letter": "A",
                        "min_score": 80.0,
                        "max_score": 100.0,
                        "points": 12,
                        "comment": "Excellent"
                    },
                    ...
                ]
            }
        """
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