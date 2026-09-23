from django.core.management.base import BaseCommand
from hospitals.models import Hospital


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        image_map = {

            # Older hospitals
            "City Care Hospital": "city-care-hospital.jpg",
            "Sunrise Multispeciality Hospital": "sunrise-hospital.jpg",
            "Green Valley Hospital": "green-valley-hospital.jpg",
            "Apex Medical Centre": "apex-medical-centre.jpg",
            "Harmony Healthcare Hospital": "harmony-healthcare.jpg",
            "LifeLine Super Speciality Hospital": "lifeline-hospital.jpg",

            # New hospitals
            "Ludhiana City Medical Centre": "ludhiana-city-medical.jpg",
            "Punjab Care Hospital": "punjab-care-hospital.jpg",
            "Jalandhar Health Centre": "jalandhar-health-centre.jpg",
            "Doaba Multispeciality Centre": "doaba-multispeciality.jpg",
            "Amritsar Medical Centre": "amritsar-medical-centre.jpg",
            "Golden Care Hospital": "golden-care-hospital.jpg",
            "Chandigarh Health Institute": "chandigarh-health-institute.jpg",
            "Tricity Medical Centre": "tricity-medical-centre.jpg",
            "Mohali Medical Hub": "mohali-medical-hub.jpg",
            "Patiala Care Hospital": "patiala-care-hospital.jpg",
            "Hoshiarpur Medical Centre": "hoshiarpur-medical-centre.jpg",
            "Delhi Advanced Medical Centre": "delhi-advanced-medical.jpg",
        }

        updated = 0

        for hospital_name, image_name in image_map.items():

            hospital = Hospital.objects.filter(
                name=hospital_name
            ).first()

            if hospital:

                hospital.image_name = image_name

                hospital.save(
                    update_fields=["image_name"]
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Assigned: {hospital_name} -> {image_name}"
                    )
                )

                updated += 1

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Hospital not found: {hospital_name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully assigned {updated} hospital images."
            )
        )