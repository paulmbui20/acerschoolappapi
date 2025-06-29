from django.db import migrations

def populate_sample_grades(apps, schema_editor):
    SampleGrade = apps.get_model('sample', 'SampleGrade')
    kcse_grades = [
        {'grade_letter': 'A', 'min_score': 80.0, 'max_score': 100.0, 'points': 12, 'comment': 'Excellent'},
        {'grade_letter': 'A-', 'min_score': 75.0, 'max_score': 80.0, 'points': 11, 'comment': 'Very Good'},
        {'grade_letter': 'B+', 'min_score': 70.0, 'max_score': 75.0, 'points': 10, 'comment': 'Good'},
        {'grade_letter': 'B', 'min_score': 65.0, 'max_score': 70.0, 'points': 9, 'comment': 'Above Average'},
        {'grade_letter': 'B-', 'min_score': 60.0, 'max_score': 65.0, 'points': 8, 'comment': 'Average'},
        {'grade_letter': 'C+', 'min_score': 55.0, 'max_score': 60.0, 'points': 7, 'comment': 'Fairly Good'},
        {'grade_letter': 'C', 'min_score': 50.0, 'max_score': 55.0, 'points': 6, 'comment': 'Fair'},
        {'grade_letter': 'C-', 'min_score': 45.0, 'max_score': 50.0, 'points': 5, 'comment': 'Below Average'},
        {'grade_letter': 'D+', 'min_score': 40.0, 'max_score': 45.0, 'points': 4, 'comment': 'Poor'},
        {'grade_letter': 'D', 'min_score': 35.0, 'max_score': 40.0, 'points': 3, 'comment': 'Very Poor'},
        {'grade_letter': 'D-', 'min_score': 30.0, 'max_score': 35.0, 'points': 2, 'comment': 'Extremely Poor'},
        {'grade_letter': 'E', 'min_score': 0.0, 'max_score': 30.0, 'points': 1, 'comment': 'Fail'},
    ]
    for grade in kcse_grades:
        SampleGrade.objects.create(**grade)

class Migration(migrations.Migration):
    dependencies = [
        ('sample', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(populate_sample_grades),
    ]