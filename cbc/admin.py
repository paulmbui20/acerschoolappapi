from django.contrib import admin
from django.db.models.functions import Lower
from .models import LearningArea, LearningLevel


@admin.register(LearningArea)
class LearningAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    # list_filter = ()
    ordering = (Lower("name"),)
    # readonly_fields = ()
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(lower_name=Lower("name")).order_by("lower_name")


@admin.register(LearningLevel)
class LearningLevelsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = (Lower("name"),)
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(lower_name=Lower("name")).order_by("lower_name")
