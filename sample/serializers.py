from rest_framework import serializers
from .models import SampleSubject, SampleKCSESubjectPaper

class SampleKCSESubjectPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleKCSESubjectPaper
        fields = ['paper_name', 'max_score', 'percentage_weight']


class SampleSubjectSerializer(serializers.ModelSerializer):
    papers = SampleKCSESubjectPaperSerializer(many=True, source='samplekcsesubjectpaper_set', read_only=True)

    class Meta:
        model = SampleSubject
        fields = ['subject_code', 'name', 'papers']

