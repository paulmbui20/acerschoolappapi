from django.db import models


class SampleGrade(models.Model):
    grade_letter = models.CharField(max_length=10, unique=True)
    min_score = models.FloatField()
    max_score = models.FloatField()
    points = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-max_score']

    def __str__(self):
        return f"{self.grade_letter} ({self.min_score}-{self.max_score})"


class SampleSubject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject_code = models.CharField(max_length=10, unique=True)
    class Meta:
        ordering = ['subject_code']

    def __str__(self):
        return f"{self.name} - {self.subject_code}"


class SampleKCSESubjectPaper(models.Model):
    PAPER_CHOICES = [
        ('Paper 1', 'Paper 1'),
        ('Paper 2', 'Paper 2'),
        ('Paper 3', 'Paper 3'),
    ]

    subject = models.ForeignKey(SampleSubject, on_delete=models.CASCADE, related_name='samplekcsesubjectpaper_set')
    paper_name = models.CharField(max_length=20, choices=PAPER_CHOICES)
    max_score = models.PositiveIntegerField()
    percentage_weight = models.FloatField(help_text="Percentage weight towards final grade")

    class Meta:
        unique_together = ('subject', 'paper_name')
        verbose_name = 'KCSE Subject Paper'
        verbose_name_plural = 'KCSE Subject Papers'

    def __str__(self):
        return f"{self.subject.name} - {self.paper_name} ({self.percentage_weight}%)"
