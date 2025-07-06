from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator


class CustomThrottle(AnonRateThrottle):
    scope = 'custom'
    rate = '30/hour'


class BaseAPIView(APIView):
    """
    Base API view with common functionality for all endpoints
    """
    throttle_classes = [CustomThrottle, UserRateThrottle]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    @method_decorator(cache_page(60 * 15))
    @method_decorator(vary_on_headers('Authorization', 'Cookie'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)