from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from cbc.models import LearningLevel

LEARNING_LEVELS = [
    "Pre-Primary 1",
    "Pre-Primary 2",
    "Grade 1",
    "Grade 2",
    "Grade 3",
    "Grade 4",
    "Grade 5",
    "Grade 6",
    "Grade 7",
    "Grade 8",
    "Grade 9",
]

class Command(BaseCommand):
    help = "Populate CBC/CBE Learning Levels (e.g., Grade 1–9) with safe handling."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting Learning Levels population..."))

        created_count = 0
        skipped_count = 0

        with transaction.atomic():
            for level in LEARNING_LEVELS:
                try:
                    obj, created = LearningLevel.objects.get_or_create(
                        name=level.strip()
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(self.style.SUCCESS(f"Created: {level}"))
                    else:
                        skipped_count += 1
                        self.stdout.write(self.style.WARNING(f"Skipped (exists): {level}"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(
                        f"Integrity error for: {level}, check uniqueness rules."
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Unexpected error for {level}: {str(e)}"
                    ))

        self.stdout.write(self.style.SUCCESS(
            f"Completed. Created: {created_count}, Skipped: {skipped_count}"
        ))
