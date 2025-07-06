from django.db import models
from django.utils import timezone


class AnalyticsRecord(models.Model):
    """Model to store analytics data received from schools"""
    school_details = models.JSONField()
    data = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def mark_as_processed(self):
        self.processed_at = timezone.now()
        self.is_processed = True
        self.save(update_fields=['processed_at', 'is_processed'])

    def __str__(self):
        return f"Analytics from {self.school} at {self.received_at}"

    class Meta:
        indexes = [
            models.Index(fields=['school_details', 'received_at', 'is_processed']),
        ]