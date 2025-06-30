from rest_framework.response import Response

from sample.functions.rest_framework import BaseAPIView
from sample.models import SampleSubject
from sample.serializers import SampleSubjectSerializer


class KCSEPapersList(BaseAPIView):
    """
    API endpoint for retrieving KCSE subjects with their associated papers.
    
    This endpoint provides access to all KCSE subjects along with their associated papers,
    including paper names, maximum scores, and percentage weights. The data is structured
    to show the relationship between subjects and their papers.
    
    Throttling:
        - Anonymous users: 60 requests per hour
        - Authenticated users: Default DRF rate limits
    
    Caching:
        Results are cached for 15 minutes to improve performance.
    """
    
    def get(self, request, *args, **kwargs):
        """
        Retrieve all KCSE subjects with their papers grouped together.
        
        This method returns a comprehensive list of all subjects in the KCSE curriculum,
        along with their associated papers. Each subject includes details about its papers,
        such as paper name, maximum score, and percentage weight towards the final grade.
        
        Parameters:
            request (Request): The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        
        Returns:
            Response: A JSON response containing:
                - subjects (list): List of subject objects with the following fields:
                    - subject_code (str): The subject code
                    - name (str): The subject name
                    - papers (list): List of paper objects with the following fields:
                        - paper_name (str): The paper name (e.g., 'Paper 1', 'Paper 2')
                        - max_score (int): Maximum score possible for this paper
                        - percentage_weight (float): Percentage weight towards final grade
        
        Example Response:
            {
                "subjects": [
                    {
                        "subject_code": "MATH",
                        "name": "Mathematics",
                        "papers": [
                            {
                                "paper_name": "Paper 1",
                                "max_score": 100,
                                "percentage_weight": 50.0
                            },
                            {
                                "paper_name": "Paper 2",
                                "max_score": 100,
                                "percentage_weight": 50.0
                            }
                        ]
                    },
                    ...
                ]
            }
        """
        subjects = SampleSubject.objects.prefetch_related('samplekcsesubjectpaper_set').all()
        serializer = SampleSubjectSerializer(subjects, many=True)
        return Response({
            'subjects': serializer.data
        })