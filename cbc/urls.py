from django.urls import path
from .views import (
    LearningAreaListView,
    LearningAreaDetailView,
    LearningLevelsListView,
    LearningLevelDetailView,
)

urlpatterns = [
    path("sample/learning-areas/", LearningAreaListView.as_view(), name="learningarea-list"),
    path("sample/learning-areas/<int:id>/", LearningAreaDetailView.as_view(), name="learningarea-detail"),

    path("sample/learning-levels/", LearningLevelsListView.as_view(), name="learninglevels-list"),
    path("sample/learning-levels/<int:id>/", LearningLevelDetailView.as_view(), name="learninglevels-detail"),
]
