from django.core.management.base import BaseCommand
from hospitals.models import Treatment


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        treatments = [

            {
                "name": "Cataract Surgery",
                "department": "Ophthalmology",
                "min_cost": 30000,
                "max_cost": 60000,
                "patients_treated": 1250,
                "success_rate": 96.50,
                "description": "Surgical treatment for cataracts to improve vision and restore lens clarity."
            },

            {
                "name": "Knee Replacement",
                "department": "Orthopedics",
                "min_cost": 120000,
                "max_cost": 250000,
                "patients_treated": 850,
                "success_rate": 94.20,
                "description": "Replacement of a damaged knee joint to improve mobility and reduce pain."
            },

            {
                "name": "Angioplasty",
                "department": "Cardiology",
                "min_cost": 150000,
                "max_cost": 300000,
                "patients_treated": 720,
                "success_rate": 93.80,
                "description": "A cardiovascular procedure used to restore blood flow through narrowed arteries."
            },

            {
                "name": "Appendectomy",
                "department": "General Surgery",
                "min_cost": 40000,
                "max_cost": 90000,
                "patients_treated": 980,
                "success_rate": 97.10,
                "description": "Surgical removal of the appendix, commonly performed for appendicitis."
            },

            {
                "name": "Kidney Stone Treatment",
                "department": "Urology",
                "min_cost": 25000,
                "max_cost": 80000,
                "patients_treated": 1100,
                "success_rate": 95.30,
                "description": "Medical and surgical treatment options for removing or managing kidney stones."
            },

            {
                "name": "Diabetes Management",
                "department": "General Medicine",
                "min_cost": 5000,
                "max_cost": 25000,
                "patients_treated": 2100,
                "success_rate": 91.50,
                "description": "Long-term management of blood glucose levels through monitoring, medication and lifestyle care."
            },

            {
                "name": "Skin Allergy Treatment",
                "department": "Dermatology",
                "min_cost": 3000,
                "max_cost": 15000,
                "patients_treated": 1650,
                "success_rate": 92.80,
                "description": "Diagnosis and treatment of common allergic and inflammatory skin conditions."
            },

            {
                "name": "Pediatric Fever Treatment",
                "department": "Pediatrics",
                "min_cost": 2000,
                "max_cost": 10000,
                "patients_treated": 1850,
                "success_rate": 94.60,
                "description": "Assessment and treatment of fever and common infections in children."
            },

            {
                "name": "MRI Scan",
                "department": "Radiology",
                "min_cost": 5000,
                "max_cost": 12000,
                "patients_treated": 3200,
                "success_rate": 98.20,
                "description": "Advanced imaging used to create detailed images of organs, tissues and other structures."
            },

            {
                "name": "CT Scan",
                "department": "Radiology",
                "min_cost": 3000,
                "max_cost": 9000,
                "patients_treated": 4100,
                "success_rate": 98.50,
                "description": "Computed tomography imaging used for detailed examination of internal body structures."
            },

            {
                "name": "Ultrasound",
                "department": "Radiology",
                "min_cost": 1000,
                "max_cost": 3500,
                "patients_treated": 5200,
                "success_rate": 99.00,
                "description": "Non-invasive imaging procedure used to examine internal organs and tissues."
            },

            {
                "name": "Normal Delivery",
                "department": "Gynecology",
                "min_cost": 25000,
                "max_cost": 60000,
                "patients_treated": 1800,
                "success_rate": 97.50,
                "description": "Hospital-supported vaginal delivery with maternal and newborn care."
            },

            {
                "name": "Cesarean Section",
                "department": "Gynecology",
                "min_cost": 50000,
                "max_cost": 100000,
                "patients_treated": 1200,
                "success_rate": 96.80,
                "description": "Surgical delivery of a baby through an incision in the abdomen and uterus."
            },

            {
                "name": "Gallbladder Surgery",
                "department": "General Surgery",
                "min_cost": 60000,
                "max_cost": 120000,
                "patients_treated": 760,
                "success_rate": 95.80,
                "description": "Surgical removal of the gallbladder, commonly performed for gallstones."
            },

            {
                "name": "Hernia Repair",
                "department": "General Surgery",
                "min_cost": 45000,
                "max_cost": 90000,
                "patients_treated": 890,
                "success_rate": 96.20,
                "description": "Surgical repair of weakened tissue that causes an abdominal or groin hernia."
            },

            {
                "name": "Heart Bypass Surgery",
                "department": "Cardiology",
                "min_cost": 250000,
                "max_cost": 500000,
                "patients_treated": 430,
                "success_rate": 92.60,
                "description": "Major cardiac surgery that creates a new route for blood flow around blocked coronary arteries."
            },

            {
                "name": "Pacemaker Implantation",
                "department": "Cardiology",
                "min_cost": 100000,
                "max_cost": 250000,
                "patients_treated": 380,
                "success_rate": 94.10,
                "description": "Procedure for implanting a device that helps regulate abnormal heart rhythms."
            },

            {
                "name": "Stroke Rehabilitation",
                "department": "Neurology",
                "min_cost": 20000,
                "max_cost": 80000,
                "patients_treated": 640,
                "success_rate": 88.50,
                "description": "Rehabilitation program supporting recovery of movement, speech and daily functions after stroke."
            },

            {
                "name": "Migraine Treatment",
                "department": "Neurology",
                "min_cost": 3000,
                "max_cost": 15000,
                "patients_treated": 1400,
                "success_rate": 90.40,
                "description": "Evaluation and management of recurring migraine headaches and related symptoms."
            },

            {
                "name": "Physiotherapy",
                "department": "Physiotherapy",
                "min_cost": 500,
                "max_cost": 2000,
                "patients_treated": 3600,
                "success_rate": 93.20,
                "description": "Physical rehabilitation designed to improve movement, strength and recovery."
            },

            {
                "name": "Dental Root Canal",
                "department": "Dental",
                "min_cost": 4000,
                "max_cost": 12000,
                "patients_treated": 1900,
                "success_rate": 95.50,
                "description": "Dental procedure used to treat infection or damage inside a tooth."
            },

            {
                "name": "Dental Implant",
                "department": "Dental",
                "min_cost": 25000,
                "max_cost": 60000,
                "patients_treated": 620,
                "success_rate": 94.70,
                "description": "Replacement of a missing tooth using an artificial dental implant."
            },

            {
                "name": "Acne Treatment",
                "department": "Dermatology",
                "min_cost": 2000,
                "max_cost": 12000,
                "patients_treated": 2100,
                "success_rate": 91.80,
                "description": "Medical management of acne and related skin inflammation."
            },

            {
                "name": "ENT Infection Treatment",
                "department": "ENT",
                "min_cost": 2000,
                "max_cost": 10000,
                "patients_treated": 1750,
                "success_rate": 93.60,
                "description": "Diagnosis and treatment of common ear, nose and throat infections."
            },

            {
                "name": "Tonsil Surgery",
                "department": "ENT",
                "min_cost": 30000,
                "max_cost": 70000,
                "patients_treated": 510,
                "success_rate": 95.10,
                "description": "Surgical removal of tonsils when recurrent or severe tonsil problems require treatment."
            },

            {
                "name": "Asthma Management",
                "department": "Pulmonology",
                "min_cost": 3000,
                "max_cost": 15000,
                "patients_treated": 1600,
                "success_rate": 90.90,
                "description": "Diagnosis, monitoring and long-term management of asthma symptoms."
            },

            {
                "name": "Pneumonia Treatment",
                "department": "Pulmonology",
                "min_cost": 10000,
                "max_cost": 40000,
                "patients_treated": 1250,
                "success_rate": 92.70,
                "description": "Medical treatment and monitoring for pneumonia and respiratory infection."
            },

            {
                "name": "Thyroid Treatment",
                "department": "Endocrinology",
                "min_cost": 5000,
                "max_cost": 25000,
                "patients_treated": 1300,
                "success_rate": 92.40,
                "description": "Diagnosis and management of thyroid disorders and hormone-related conditions."
            },

            {
                "name": "Blood Pressure Management",
                "department": "General Medicine",
                "min_cost": 3000,
                "max_cost": 15000,
                "patients_treated": 2500,
                "success_rate": 93.10,
                "description": "Monitoring and management of high blood pressure through medical and lifestyle care."
            },

            {
                "name": "Fracture Treatment",
                "department": "Orthopedics",
                "min_cost": 15000,
                "max_cost": 70000,
                "patients_treated": 1150,
                "success_rate": 94.80,
                "description": "Assessment and treatment of bone fractures using appropriate orthopedic care."
            },

        ]

        added = 0
        updated = 0

        for data in treatments:

            treatment, created = Treatment.objects.update_or_create(
                name=data["name"],
                defaults={
                    "department": data["department"],
                    "min_cost": data["min_cost"],
                    "max_cost": data["max_cost"],
                    "patients_treated": data["patients_treated"],
                    "success_rate": data["success_rate"],
                    "description": data["description"],
                }
            )

            if created:
                added += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added: {treatment.name}"
                    )
                )
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nAdded {added} new treatments."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} existing treatments."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total treatments in database: "
                f"{Treatment.objects.count()}"
            )
        )