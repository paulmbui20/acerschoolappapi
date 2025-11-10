from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower
from cbc.models import LearningArea

CBC_LEARNING_AREAS = [
    ("Mathematics", "MATH"),
    ("English", "ENG"),
    ("Kiswahili", "KISW"),
    ("Kenya Sign Language", "KSL"),
    ("Home Science", "HSC"),
    ("Social Studies", "SST"),
    ("Science and Technology", "SCT"),
    ("Integrated Science", "INT_SCI"),
    ("Pre-Technical Studies", "PRETECH"),
    ("Agriculture & Nutrition", "AGR_NUT"),
    ("Music", "MUS"),
    ("Creative Arts & Sports", "ART_SPORTS"),
    ("Physical and Health Education", "PHE"),
    ("CRE", "CRE"),
    ("IRE", "IRE"),
    ("HRE", "HRE"),
]


class Command(BaseCommand):
    help = "Populate CBC Learning Areas for Kenya with safe idempotent handling."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting CBC Learning Areas population..."))

        created_count = 0
        skipped_count = 0

        with transaction.atomic():
            for name, code in CBC_LEARNING_AREAS:
                try:
                    obj, created = LearningArea.objects.get_or_create(
                        name=name.strip(),
                        defaults={"code": code.strip()}
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Created: {name} ({code})"))
                    else:
                        skipped_count += 1
                        self.stdout.write(self.style.WARNING(f"Skipped (exists): {name}"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(
                        f"Integrity error for entry: {name} – check uniqueness rules."
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Unexpected error for {name}: {str(e)}"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"Completed. Created: {created_count}, Skipped: {skipped_count}"
        ))
