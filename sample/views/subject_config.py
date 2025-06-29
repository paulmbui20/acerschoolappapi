from rest_framework.response import Response

from sample.functions.rest_framework import BaseAPIView
from sample.models import SampleSubject
from sample.serializers import SampleSubjectSerializer


class KCSEPapersList(BaseAPIView):
    def get(self, request, *args, **kwargs):
        """Get all KCSE subjects with their papers grouped together"""
        subjects = SampleSubject.objects.prefetch_related('samplekcsesubjectpaper_set').all()
        serializer = SampleSubjectSerializer(subjects, many=True)
        return Response({
            'subjects': serializer.data
        })