from django.core.cache import cache
from django.db.models.functions import Lower
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import LearningArea, LearningLevel
from .serializers import LearningAreaSerializer, LearningLevelsSerializer

CACHE_TTL = 60 * 24 * 30  # 30 days


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CachedListMixin:
    cache_key = None

    def list(self, request, *args, **kwargs):
        # Include query parameters in cache key for pagination/filtering
        cache_key = self.get_cache_key(request)

        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)

        response = super().list(request, *args, **kwargs)
        # Cache the complete response data (including pagination structure)
        cache.set(cache_key, response.data, CACHE_TTL)
        return response

    def get_cache_key(self, request):
        # Include query parameters in cache key to handle different pagination/filtering
        base_key = self.cache_key
        query_params = request.GET.urlencode()
        if query_params:
            return f"{base_key}_{query_params}"
        return base_key


class CachedDetailMixin:
    model_name = None

    def retrieve(self, request, *args, **kwargs):
        obj_id = kwargs.get("id")
        key = f"{self.model_name}_detail_{obj_id}"

        cached_data = cache.get(key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(key, response.data, CACHE_TTL)
        return response


class BaseReadOnlyAPIView:
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = StandardPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(lower_name=Lower("name")).order_by("lower_name")


class LearningAreaListView(CachedListMixin, BaseReadOnlyAPIView, generics.ListAPIView):
    queryset = LearningArea.objects.all()
    serializer_class = LearningAreaSerializer
    cache_key = "learningarea_list"


class LearningLevelsListView(CachedListMixin, BaseReadOnlyAPIView, generics.ListAPIView):
    queryset = LearningLevel.objects.all()
    serializer_class = LearningLevelsSerializer
    cache_key = "learninglevels_list"


class LearningAreaDetailView(CachedDetailMixin, BaseReadOnlyAPIView, generics.RetrieveAPIView):
    queryset = LearningArea.objects.all()
    serializer_class = LearningAreaSerializer
    lookup_url_kwarg = "id"
    model_name = "learningarea"


class LearningLevelDetailView(CachedDetailMixin, BaseReadOnlyAPIView, generics.RetrieveAPIView):
    queryset = LearningLevel.objects.all()
    serializer_class = LearningLevelsSerializer
    lookup_url_kwarg = "id"
    model_name = "learninglevel"
