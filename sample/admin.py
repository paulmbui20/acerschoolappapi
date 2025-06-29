from django.contrib import admin

from sample.models import SampleGrade, SampleKCSESubjectPaper, SampleSubject

@admin.register(SampleGrade)
class SampleGradeAdmin(admin.ModelAdmin):
    list_display = ('grade_letter', 'min_score', 'max_score', 'points', 'comment')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('grade_letter', 'points',)

class SampleKCSESubjectPaperInline(admin.TabularInline):
    model = SampleKCSESubjectPaper
    extra = 1  # Number of empty forms to display
    fields = ('paper_name', 'max_score', 'percentage_weight')
    # min_num = 1  # Require at least one paper
    can_delete = True  # Allow deleting papers

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Add validation to ensure percentage weights sum to 100
        class PaperFormset(formset):
            def clean(self):
                super().clean()
                if any(self.errors):
                    return
                total_weight = sum(form.cleaned_data.get('percentage_weight', 0) for form in self.forms if not form.cleaned_data.get('DELETE', False))
                if abs(total_weight - 100.0) > 0.01:  # Allow small float precision errors
                    raise forms.ValidationError("The sum of percentage weights for all papers must equal 100%.")
        return PaperFormset


@admin.register(SampleSubject)
class SampleSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'name', 'paper_count')
    list_display_links = ('name','subject_code')
    list_filter = ('name',)
    search_fields = ('subject_code', 'name')
    inlines = [SampleKCSESubjectPaperInline]

    def paper_count(self, obj):
        return obj.samplekcsesubjectpaper_set.count()
    paper_count.short_description = 'Number of Papers'

