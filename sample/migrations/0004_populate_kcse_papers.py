from django.db import migrations

def populate_kcse_subject_papers(apps, schema_editor):
    SampleSubject = apps.get_model('sample', 'SampleSubject')
    SampleKCSESubjectPaper = apps.get_model('sample', 'SampleKCSESubjectPaper')

    subjects_data = [
        {
            'subject_code': '101',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 60, 'percentage_weight': 30.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 60, 'percentage_weight': 30.0},
            ]
        },
        {
            'subject_code': '102',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 60, 'percentage_weight': 30.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 60, 'percentage_weight': 30.0},
            ]
        },
        {
            'subject_code': '121',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '231',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 40, 'percentage_weight': 20.0},
            ]
        },
        {
            'subject_code': '232',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 40, 'percentage_weight': 20.0},
            ]
        },
        {
            'subject_code': '233',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 40, 'percentage_weight': 20.0},
            ]
        },
        {
            'subject_code': '311',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '312',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '313',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '314',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '443',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '451',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '501',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '503',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '504',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 60, 'percentage_weight': 30.0},
                {'paper_name': 'Paper 2', 'max_score': 80, 'percentage_weight': 40.0},
                {'paper_name': 'Paper 3', 'max_score': 60, 'percentage_weight': 30.0},
            ]
        },
        {
            'subject_code': '511',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
        {
            'subject_code': '565',
            'papers': [
                {'paper_name': 'Paper 1', 'max_score': 100, 'percentage_weight': 50.0},
                {'paper_name': 'Paper 2', 'max_score': 100, 'percentage_weight': 50.0},
            ]
        },
    ]

    for subject_data in subjects_data:
        try:
            subject = SampleSubject.objects.get(subject_code=subject_data['subject_code'])
            for paper_data in subject_data['papers']:
                SampleKCSESubjectPaper.objects.get_or_create(
                    subject=subject,
                    paper_name=paper_data['paper_name'],
                    defaults={
                        'max_score': paper_data['max_score'],
                        'percentage_weight': paper_data['percentage_weight']
                    }
                )
        except SampleSubject.DoesNotExist:
            # Log or skip if subject is not found
            print(f"Subject with code {subject_data['subject_code']} not found, skipping paper creation.")

class Migration(migrations.Migration):
    dependencies = [
        ('sample', '0003_populate_sample_subjects'),
    ]

    operations = [
        migrations.RunPython(populate_kcse_subject_papers),
    ]