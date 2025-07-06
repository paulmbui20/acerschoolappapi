from django.contrib import admin
from .models import AnalyticsRecord

@admin.register(AnalyticsRecord)
class AnalyticsRecordAdmin(admin.ModelAdmin):
    '''Admin View for AnalyticsRecord'''
    pass