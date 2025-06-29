from django.db import migrations


def create_sample_subjects(apps, schema_editor):
    SampleSubject = apps.get_model('sample', 'SampleSubject')

    subjects = [
        {'name': 'English', 'subject_code': '101'},
        {'name': 'Kiswahili', 'subject_code': '102'},
        {'name': 'Mathematics', 'subject_code': '121'},
        {'name': 'Biology', 'subject_code': '231'},
        {'name': 'Physics', 'subject_code': '232'},
        {'name': 'Chemistry', 'subject_code': '233'},
        {'name': 'Christian Religious Education', 'subject_code': '313'},
        {'name': 'History and Government', 'subject_code': '311'},
        {'name': 'Geography', 'subject_code': '312'},
        {'name': 'Islamic Religious Education', 'subject_code': '314'},
        {'name': 'Hindu Religious Education', 'subject_code': '315'},
        {'name': 'Business Studies', 'subject_code': '565'},
        {'name': 'Agriculture', 'subject_code': '443'},
        {'name': 'Home Science', 'subject_code': '441'},
        {'name': 'Computer Studies', 'subject_code': '451'},
        {'name': 'Art and Design', 'subject_code': '442'},
        {'name': 'Music', 'subject_code': '511'},
        {'name': 'Arabic', 'subject_code': '501'},
        {'name': 'German', 'subject_code': '502'},
        {'name': 'French', 'subject_code': '503'},
        {'name': 'Kenya Sign Language', 'subject_code': '504'},
        {'name': 'Aviation Technology', 'subject_code': '447'},
        {'name': 'Building Construction', 'subject_code': '444'},
        {'name': 'Electricity', 'subject_code': '445'},
        {'name': 'Drawing and Design', 'subject_code': '446'},
        {'name': 'Power Mechanics', 'subject_code': '448'},
        {'name': 'Woodwork', 'subject_code': '449'},
        {'name': 'Metalwork', 'subject_code': '450'},
        {'name': 'Commerce', 'subject_code': '566'},
        {'name': 'Accounting', 'subject_code': '567'},
        {'name': 'Economics', 'subject_code': '568'},
        {'name': 'Office Practice', 'subject_code': '569'},
        {'name': 'Shorthand', 'subject_code': '570'},
        {'name': 'Typewriting', 'subject_code': '571'},
        {'name': 'Foreign Languages', 'subject_code': '500'},
        {'name': 'Indigenous Languages', 'subject_code': '520'},
    ]

    for subject in subjects:
        SampleSubject.objects.create(**subject)


class Migration(migrations.Migration):
    dependencies = [
        ('sample', '0002_populate_sample_grades'),
    ]

    operations = [
        migrations.RunPython(create_sample_subjects),
    ]
