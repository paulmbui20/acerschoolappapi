#!/usr/bin/env python
import os
import csv
import json
import argparse
from datetime import datetime

# Check if we're in Django or FastAPI environment
try:
    # Django imports
    import django
    from django.conf import settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acerschoolappapi.settings')
    django.setup()
    from sample.models import SampleGrade, SampleSubject, SampleKCSESubjectPaper
    from analytics.models import AnalyticsRecord
    USING_DJANGO = True
except ImportError:
    # FastAPI imports
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from fastapi.app.models import get_db, SampleGrade, SampleSubject, SampleKCSESubjectPaper, AnalyticsRecord
    from fastapi.app.models.base import Base
    import os
    from dotenv import load_dotenv
    load_dotenv()
    USING_DJANGO = False
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/acerschoolapp")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def export_to_csv(model_name, queryset, fieldnames, output_dir="exports"):
    """Export a queryset to CSV"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{model_name}_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in queryset:
            row = {}
            for field in fieldnames:
                value = getattr(item, field)
                # Handle JSON fields
                if isinstance(value, dict):
                    row[field] = json.dumps(value)
                # Handle datetime fields
                elif hasattr(value, 'isoformat'):
                    row[field] = value.isoformat()
                else:
                    row[field] = value
            writer.writerow(row)
    
    print(f"Exported {model_name} to {filename}")
    return filename


def import_from_csv(model_class, csv_file, django_model=None):
    """Import data from CSV to database"""
    imported_count = 0
    
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        if USING_DJANGO:
            for row in reader:
                # Handle JSON fields
                for field in row:
                    if field in ['school_details', 'data']:
                        try:
                            row[field] = json.loads(row[field])
                        except (json.JSONDecodeError, TypeError):
                            pass
                
                # Create or update the object
                obj, created = django_model.objects.update_or_create(
                    id=row['id'],
                    defaults=row
                )
                imported_count += 1
        else:
            db = SessionLocal()
            try:
                for row in reader:
                    # Handle JSON fields
                    for field in row:
                        if field in ['school_details', 'data']:
                            try:
                                row[field] = json.loads(row[field])
                            except (json.JSONDecodeError, TypeError):
                                pass
                        # Handle boolean fields
                        elif field == 'is_processed':
                            row[field] = row[field].lower() == 'true'
                    
                    # Check if object exists
                    obj = db.query(model_class).filter(model_class.id == row['id']).first()
                    
                    if obj:
                        # Update existing object
                        for key, value in row.items():
                            setattr(obj, key, value)
                    else:
                        # Create new object
                        obj = model_class(**row)
                        db.add(obj)
                    
                    imported_count += 1
                
                db.commit()
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
    
    print(f"Imported {imported_count} records from {csv_file}")
    return imported_count


def export_all_models(output_dir="exports"):
    """Export all models to CSV files"""
    if USING_DJANGO:
        # Export SampleGrade
        grades = SampleGrade.objects.all()
        export_to_csv('sample_grades', grades, 
                     ['id', 'grade_letter', 'min_score', 'max_score', 'points', 'comment', 'created_at', 'updated_at'], 
                     output_dir)
        
        # Export SampleSubject
        subjects = SampleSubject.objects.all()
        export_to_csv('sample_subjects', subjects, 
                     ['id', 'name', 'subject_code'], 
                     output_dir)
        
        # Export SampleKCSESubjectPaper
        papers = SampleKCSESubjectPaper.objects.all()
        export_to_csv('sample_kcse_papers', papers, 
                     ['id', 'subject_id', 'paper_name', 'max_score', 'percentage_weight'], 
                     output_dir)
        
        # Export AnalyticsRecord
        analytics = AnalyticsRecord.objects.all()
        export_to_csv('analytics_records', analytics, 
                     ['id', 'school_details', 'data', 'received_at', 'processed_at', 'is_processed', 'created_at', 'updated_at'], 
                     output_dir)
    else:
        db = SessionLocal()
        try:
            # Export SampleGrade
            grades = db.query(SampleGrade).all()
            export_to_csv('sample_grades', grades, 
                         ['id', 'grade_letter', 'min_score', 'max_score', 'points', 'comment', 'created_at', 'updated_at'], 
                         output_dir)
            
            # Export SampleSubject
            subjects = db.query(SampleSubject).all()
            export_to_csv('sample_subjects', subjects, 
                         ['id', 'name', 'subject_code', 'created_at', 'updated_at'], 
                         output_dir)
            
            # Export SampleKCSESubjectPaper
            papers = db.query(SampleKCSESubjectPaper).all()
            export_to_csv('sample_kcse_papers', papers, 
                         ['id', 'subject_id', 'paper_name', 'max_score', 'percentage_weight', 'created_at', 'updated_at'], 
                         output_dir)
            
            # Export AnalyticsRecord
            analytics = db.query(AnalyticsRecord).all()
            export_to_csv('analytics_records', analytics, 
                         ['id', 'school_details', 'data', 'received_at', 'processed_at', 'is_processed', 'created_at', 'updated_at'], 
                         output_dir)
        finally:
            db.close()


def import_all_models(input_dir):
    """Import all models from CSV files in the specified directory"""
    if not os.path.exists(input_dir):
        print(f"Error: Directory {input_dir} does not exist")
        return
    
    # Get the latest file for each model
    files = os.listdir(input_dir)
    latest_files = {}
    
    for file in files:
        if not file.endswith('.csv'):
            continue
        
        model_name = file.split('_')[0]
        if model_name not in latest_files or file > latest_files[model_name]:
            latest_files[model_name] = file
    
    # Import in the correct order (to handle foreign keys)
    if 'sample_grades' in latest_files:
        if USING_DJANGO:
            import_from_csv(SampleGrade, os.path.join(input_dir, latest_files['sample_grades']), django_model=SampleGrade)
        else:
            import_from_csv(SampleGrade, os.path.join(input_dir, latest_files['sample_grades']))
    
    if 'sample_subjects' in latest_files:
        if USING_DJANGO:
            import_from_csv(SampleSubject, os.path.join(input_dir, latest_files['sample_subjects']), django_model=SampleSubject)
        else:
            import_from_csv(SampleSubject, os.path.join(input_dir, latest_files['sample_subjects']))
    
    if 'sample_kcse_papers' in latest_files:
        if USING_DJANGO:
            import_from_csv(SampleKCSESubjectPaper, os.path.join(input_dir, latest_files['sample_kcse_papers']), django_model=SampleKCSESubjectPaper)
        else:
            import_from_csv(SampleKCSESubjectPaper, os.path.join(input_dir, latest_files['sample_kcse_papers']))
    
    if 'analytics_records' in latest_files:
        if USING_DJANGO:
            import_from_csv(AnalyticsRecord, os.path.join(input_dir, latest_files['analytics_records']), django_model=AnalyticsRecord)
        else:
            import_from_csv(AnalyticsRecord, os.path.join(input_dir, latest_files['analytics_records']))


def main():
    parser = argparse.ArgumentParser(description='Export/Import database models to/from CSV files')
    parser.add_argument('action', choices=['export', 'import'], help='Action to perform')
    parser.add_argument('--dir', default='exports', help='Directory for export/import files')
    
    args = parser.parse_args()
    
    if args.action == 'export':
        export_all_models(args.dir)
    elif args.action == 'import':
        import_all_models(args.dir)


if __name__ == '__main__':
    main()