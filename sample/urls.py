

from django.urls import path

from sample.views.sample_grades import SampleGradeAPI
from sample.views.sample_subjects import SampleSubjectAPI
from sample.views.subject_config import KCSEPapersList


urlpatterns = [
    path('subjects/', SampleSubjectAPI.as_view(), name='sample_subjects_api'),
    path('grades/', SampleGradeAPI.as_view(), name='sample_grades_api'),
    path('kcse-papers/', KCSEPapersList.as_view(), name='sample_kcse_papers'),

]
