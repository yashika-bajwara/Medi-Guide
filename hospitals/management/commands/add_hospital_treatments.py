from django.core.management.base import BaseCommand

from hospitals.models import (
    Hospital,
    Treatment,
    HospitalTreatment,
)


class Command(BaseCommand):

    help = "Connect hospitals with available treatments"

    def handle(self, *args, **options):

        treatment_map = {

            "Ludhiana City Medical Centre": [
                ("Cataract Surgery", 45000),
                ("Knee Replacement", 180000),
                ("Angioplasty", 225000),
                ("Appendectomy", 60000),
                ("Diabetes Management", 12000),
            ],

            "Punjab Care Hospital": [
                ("Knee Replacement", 170000),
                ("Appendectomy", 55000),
                ("Kidney Stone Treatment", 50000),
                ("Diabetes Management", 10000),
            ],

            "Jalandhar Health Centre": [
                ("Angioplasty", 220000),
                ("Knee Replacement", 175000),
                ("Appendectomy", 60000),
                ("Kidney Stone Treatment", 45000),
            ],

            "Doaba Multispeciality Centre": [
                ("Angioplasty", 240000),
                ("Knee Replacement", 190000),
                ("Diabetes Management", 11000),
                ("Skin Allergy Treatment", 7500),
            ],

            "Amritsar Medical Centre": [
                ("Angioplasty", 230000),
                ("Knee Replacement", 180000),
                ("Appendectomy", 65000),
                ("Diabetes Management", 12000),
            ],

            "Golden Care Hospital": [
                ("Kidney Stone Treatment", 50000),
                ("Appendectomy", 60000),
                ("Skin Allergy Treatment", 7000),
                ("Pediatric Fever Treatment", 5000),
            ],

            "Chandigarh Health Institute": [
                ("Angioplasty", 250000),
                ("Knee Replacement", 200000),
                ("Cataract Surgery", 50000),
                ("Appendectomy", 70000),
            ],

            "Tricity Medical Centre": [
                ("Angioplasty", 240000),
                ("Kidney Stone Treatment", 55000),
                ("Diabetes Management", 15000),
                ("Pediatric Fever Treatment", 6000),
            ],

            "Mohali Medical Hub": [
                ("Knee Replacement", 185000),
                ("Appendectomy", 60000),
                ("Kidney Stone Treatment", 50000),
                ("Diabetes Management", 10000),
            ],

            "Patiala Care Hospital": [
                ("Appendectomy", 55000),
                ("Diabetes Management", 9000),
                ("Skin Allergy Treatment", 6000),
                ("Pediatric Fever Treatment", 4500),
            ],

            "Hoshiarpur Medical Centre": [
                ("Cataract Surgery", 40000),
                ("Appendectomy", 50000),
                ("Kidney Stone Treatment", 45000),
                ("Diabetes Management", 8000),
            ],

            "Delhi Advanced Medical Centre": [
                ("Angioplasty", 275000),
                ("Knee Replacement", 225000),
                ("Appendectomy", 80000),
                ("Diabetes Management", 18000),
            ],
        }

        added = 0
        skipped = 0

        for hospital_name, treatments in treatment_map.items():

            try:
                hospital = Hospital.objects.get(
                    name=hospital_name
                )

            except Hospital.DoesNotExist:

                self.stdout.write(
                    self.style.WARNING(
                        f"Hospital not found: {hospital_name}"
                    )
                )

                continue

            for treatment_name, cost in treatments:

                try:
                    treatment = Treatment.objects.get(
                        name=treatment_name
                    )

                except Treatment.DoesNotExist:

                    self.stdout.write(
                        self.style.WARNING(
                            f"Treatment not found: {treatment_name}"
                        )
                    )

                    continue

                hospital_treatment, created = (
                    HospitalTreatment.objects.get_or_create(
                        hospital=hospital,
                        treatment=treatment,
                        defaults={
                            "estimated_cost": cost,
                            "available": True,
                        }
                    )
                )

                if created:
                    added += 1

                else:
                    skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {added} hospital-treatment connections."
            )
        )

        if skipped:
            self.stdout.write(
                self.style.WARNING(
                    f"{skipped} connections already existed and were skipped."
                )
            )