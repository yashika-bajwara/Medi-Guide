from django.core.management.base import BaseCommand

from hospitals.models import Hospital


class Command(BaseCommand):

    help = "Add demo hospitals with locations to MediFind"

    def handle(self, *args, **options):

        hospitals = [

            {
                "name": "Ludhiana City Medical Centre",
                "city": "Ludhiana",
                "area": "Model Town",
                "address": "Model Town, Ludhiana, Punjab",
                "phone": "9876501001",
                "email": "ludhiana@example.com",
                "description": "Demo multi-speciality hospital for the MediFind project.",
                "facilities": "24/7 Emergency, ICU, Pharmacy, Laboratory, Ambulance, Cardiology, Orthopedics",
                "emergency": True,
                "ambulance": True,
                "rating": 4.4,
                "latitude": 30.900965,
                "longitude": 75.857277,
            },

            {
                "name": "Punjab Care Hospital",
                "city": "Ludhiana",
                "area": "Civil Lines",
                "address": "Civil Lines, Ludhiana, Punjab",
                "phone": "9876501002",
                "email": "punjabcare@example.com",
                "description": "Demo healthcare centre offering general and specialist services.",
                "facilities": "Emergency, ICU, Pharmacy, Diagnostic Centre, Laboratory, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.3,
                "latitude": 30.912000,
                "longitude": 75.846000,
            },

            {
                "name": "Jalandhar Health Centre",
                "city": "Jalandhar",
                "area": "Model Town",
                "address": "Model Town, Jalandhar, Punjab",
                "phone": "9876501003",
                "email": "jalandharhealth@example.com",
                "description": "Demo hospital providing medical and emergency services.",
                "facilities": "Emergency, ICU, Pharmacy, Laboratory, Radiology, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.2,
                "latitude": 31.326015,
                "longitude": 75.576180,
            },

            {
                "name": "Doaba Multispeciality Centre",
                "city": "Jalandhar",
                "area": "GT Road",
                "address": "GT Road, Jalandhar, Punjab",
                "phone": "9876501004",
                "email": "doaba@example.com",
                "description": "Demo multispeciality healthcare centre.",
                "facilities": "ICU, Emergency, Cardiology, Neurology, Pharmacy, Laboratory",
                "emergency": True,
                "ambulance": True,
                "rating": 4.5,
                "latitude": 31.326500,
                "longitude": 75.584000,
            },

            {
                "name": "Amritsar Medical Centre",
                "city": "Amritsar",
                "area": "Ranjit Avenue",
                "address": "Ranjit Avenue, Amritsar, Punjab",
                "phone": "9876501005",
                "email": "amritsarmedical@example.com",
                "description": "Demo hospital providing specialist and emergency care.",
                "facilities": "Emergency, ICU, Cardiology, Orthopedics, Pharmacy, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.4,
                "latitude": 31.633980,
                "longitude": 74.872260,
            },

            {
                "name": "Golden Care Hospital",
                "city": "Amritsar",
                "area": "Majitha Road",
                "address": "Majitha Road, Amritsar, Punjab",
                "phone": "9876501006",
                "email": "goldencare@example.com",
                "description": "Demo healthcare facility with diagnostic and specialist services.",
                "facilities": "Emergency, Laboratory, Pharmacy, Diagnostic Centre, ICU, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.3,
                "latitude": 31.650000,
                "longitude": 74.880000,
            },

            {
                "name": "Chandigarh Health Institute",
                "city": "Chandigarh",
                "area": "Sector 22",
                "address": "Sector 22, Chandigarh",
                "phone": "9876501007",
                "email": "chandigarhhealth@example.com",
                "description": "Demo multispeciality hospital for the MediFind project.",
                "facilities": "24/7 Emergency, ICU, Cardiology, Neurology, Pharmacy, Laboratory",
                "emergency": True,
                "ambulance": True,
                "rating": 4.6,
                "latitude": 30.733300,
                "longitude": 76.779400,
            },

            {
                "name": "Tricity Medical Centre",
                "city": "Chandigarh",
                "area": "Sector 34",
                "address": "Sector 34, Chandigarh",
                "phone": "9876501008",
                "email": "tricity@example.com",
                "description": "Demo hospital offering general and specialist healthcare.",
                "facilities": "Emergency, ICU, Pharmacy, Radiology, Laboratory, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.5,
                "latitude": 30.715000,
                "longitude": 76.760000,
            },

            {
                "name": "Mohali Medical Hub",
                "city": "Mohali",
                "area": "Phase 7",
                "address": "Phase 7, Mohali, Punjab",
                "phone": "9876501009",
                "email": "mohali@example.com",
                "description": "Demo medical centre providing specialist healthcare.",
                "facilities": "Emergency, ICU, Pharmacy, Laboratory, Orthopedics, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.2,
                "latitude": 30.704600,
                "longitude": 76.717900,
            },

            {
                "name": "Patiala Care Hospital",
                "city": "Patiala",
                "area": "Urban Estate",
                "address": "Urban Estate, Patiala, Punjab",
                "phone": "9876501010",
                "email": "patialacare@example.com",
                "description": "Demo hospital providing general and specialist medical care.",
                "facilities": "Emergency, ICU, Pharmacy, Laboratory, General Medicine, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.1,
                "latitude": 30.339800,
                "longitude": 76.386900,
            },

            {
                "name": "Hoshiarpur Medical Centre",
                "city": "Hoshiarpur",
                "area": "Model Town",
                "address": "Model Town, Hoshiarpur, Punjab",
                "phone": "9876501011",
                "email": "hoshiarpurmedical@example.com",
                "description": "Demo healthcare centre for general and emergency services.",
                "facilities": "Emergency, Pharmacy, Laboratory, Diagnostic Services, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.2,
                "latitude": 31.514300,
                "longitude": 75.911500,
            },

            {
                "name": "Delhi Advanced Medical Centre",
                "city": "Delhi",
                "area": "Dwarka",
                "address": "Dwarka, New Delhi",
                "phone": "9876501012",
                "email": "delhiadvanced@example.com",
                "description": "Demo advanced healthcare centre for the MediFind project.",
                "facilities": "24/7 Emergency, ICU, Cardiology, Neurology, Oncology, Ambulance",
                "emergency": True,
                "ambulance": True,
                "rating": 4.7,
                "latitude": 28.592100,
                "longitude": 77.046000,
            },

        ]

        added = 0
        skipped = 0

        for data in hospitals:

            hospital, created = Hospital.objects.get_or_create(
                name=data["name"],
                city=data["city"],
                defaults=data
            )

            if created:
                added += 1

            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully added {added} demo hospitals."
            )
        )

        if skipped:
            self.stdout.write(
                self.style.WARNING(
                    f"{skipped} hospitals already existed and were skipped."
                )
            )