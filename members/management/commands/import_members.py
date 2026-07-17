import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from members.models import Member


class Command(BaseCommand):
    help = "Import members from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        created_count = 0
        skipped_count = 0

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            # Debug: print actual fieldnames
            self.stdout.write(f"CSV columns: {reader.fieldnames}")
            
            for row in reader:
                # Handle different column name variants
                name = row.get("name") or row.get("NAME") or row.get("Name")
                reg_no = row.get("registration_number") or row.get("REG NO") or row.get("registration_number")
                
                name = name.strip() if name else ""
                reg_no = reg_no.strip() if reg_no else ""

                if not name or not reg_no:
                    self.stdout.write(f"Skipping empty row")
                    skipped_count += 1
                    continue

                parts = name.split()
                first_name = parts[0] if parts else ""
                last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
                username = reg_no.lower().replace("/", "-")

                if Member.objects.filter(registration_number=reg_no).exists():
                    self.stdout.write(f"Skipping {name} ({reg_no}) - already exists")
                    skipped_count += 1
                    continue

                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": f"{username}@kafuosa.local",
                    },
                )

                Member.objects.create(
                    user=user,
                    registration_number=reg_no,
                    status="approved",
                )
                self.stdout.write(f"Created: {name} ({reg_no})")
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete: {created_count} created, {skipped_count} skipped"
            )
        )
