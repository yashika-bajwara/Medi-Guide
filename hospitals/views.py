import os

from django.shortcuts import render, get_object_or_404
from django.db import models
from openai import OpenAI

from .models import (
    Hospital,
    Treatment,
    HospitalTreatment,
    ContactMessage,
)


# =========================
# HOME
# =========================

def home(request):

    hospitals = Hospital.objects.all().order_by("name")

    treatments = Treatment.objects.all().order_by("name")

    cities = (
        Hospital.objects
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )

    departments = (
        Treatment.objects
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )

    return render(
        request,
        "hospitals/home.html",
        {
            "home_hospitals": hospitals,
            "home_treatments": treatments,
            "home_cities": cities,
            "home_departments": departments,
        }
    )


# =========================
# FIND HOSPITALS
# =========================

def hospital_list(request):

    hospitals = Hospital.objects.all()

    query = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    budget = request.GET.get("budget", "").strip()
    facility = request.GET.get("facility", "").strip()
    emergency = request.GET.get("emergency", "").strip()

    # SEARCH
    if query:
        hospitals = hospitals.filter(
            models.Q(name__icontains=query)
            | models.Q(city__icontains=query)
            | models.Q(area__icontains=query)
            | models.Q(address__icontains=query)
            | models.Q(facilities__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(
                hospitaltreatment__treatment__name__icontains=query
            )
            | models.Q(
                hospitaltreatment__treatment__department__icontains=query
            )
        )

    # CITY FILTER
    if city:
        hospitals = hospitals.filter(
            city__icontains=city
        )

    # BUDGET FILTER
    if budget:
        try:
            hospitals = hospitals.filter(
                hospitaltreatment__estimated_cost__lte=float(budget)
            )
        except (ValueError, TypeError):
            pass

    # FACILITY FILTER
    if facility:
        hospitals = hospitals.filter(
            facilities__icontains=facility
        )

    # EMERGENCY FILTER
    if emergency == "true":
        hospitals = hospitals.filter(
            emergency=True
        )

    # Remove duplicate hospitals
    hospitals = hospitals.distinct()

    # Cities for dropdown
    cities = (
        Hospital.objects
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )

    # Facilities for dropdown
    all_hospitals = Hospital.objects.all()

    facility_set = set()

    for hospital in all_hospitals:

        for item in hospital.facilities.split(","):

            item = item.strip()

            if item:
                facility_set.add(item)

    facilities = sorted(facility_set)

    return render(
        request,
        "hospitals/hospitals.html",
        {
            "hospitals": hospitals,
            "cities": cities,
            "facilities": facilities,

            "search_query": query,
            "selected_city": city,
            "selected_budget": budget,
            "selected_facility": facility,
            "selected_emergency": emergency,
        }
    )
# =========================
# HOSPITAL DETAIL
# =========================

def hospital_detail(request, pk):

    hospital = get_object_or_404(
        Hospital,
        pk=pk
    )

    treatments = HospitalTreatment.objects.filter(
        hospital=hospital,
        available=True
    ).select_related(
        "treatment"
    )

    facilities = [
        facility.strip()
        for facility in hospital.facilities.split(",")
        if facility.strip()
    ]

    return render(
        request,
        "hospitals/hospital_detail.html",
        {
            "hospital": hospital,
            "treatments": treatments,
            "facilities": facilities,
        }
    )


# =========================
# TREATMENTS
# =========================

def treatments(request):

    treatment_list = Treatment.objects.all().order_by("name")

    query = request.GET.get(
        "q",
        ""
    ).strip()

    department = request.GET.get(
        "department",
        ""
    ).strip()


    if query:

        treatment_list = treatment_list.filter(
            models.Q(name__icontains=query)
            | models.Q(department__icontains=query)
            | models.Q(description__icontains=query)
        )


    if department:

        treatment_list = treatment_list.filter(
            department__icontains=department
        )


    departments = (
        Treatment.objects
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )


    return render(
        request,
        "hospitals/treatments.html",
        {
            "treatments": treatment_list,
            "departments": departments,
            "search_query": query,
            "selected_department": department,
        }
    )
# =========================
# ANALYTICS
# =========================

def analytics(request):

    treatment_list = Treatment.objects.all()

    # -------------------------
    # TOTAL PATIENTS
    # -------------------------

    total_patients = sum(
        treatment.patients_treated
        for treatment in treatment_list
    )

    # -------------------------
    # AVERAGE SUCCESS RATE
    # -------------------------

    average_success = 0

    if treatment_list:

        average_success = sum(
            float(treatment.success_rate)
            for treatment in treatment_list
        ) / len(treatment_list)

    # -------------------------
    # AVERAGE TREATMENT BUDGET
    # -------------------------

    average_budget = 0

    if treatment_list:

        average_budget = sum(
            float(treatment.average_cost())
            for treatment in treatment_list
        ) / len(treatment_list)

    return render(
        request,
        "hospitals/analytics.html",
        {
            "treatments": treatment_list,
            "total_patients": total_patients,
            "average_success": round(
                average_success,
                2
            ),
            "average_budget": round(
                average_budget,
                2
            ),
        }
    )


# =========================
# AI CHATBOT
# =========================

def chatbot(request):

    answer = None
    user_message = ""

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if not user_message:

            answer = (
                "Please enter your question."
            )

        else:

            try:

                api_key = os.environ.get(
                    "OPENAI_API_KEY"
                )

                if not api_key:

                    raise Exception(
                        "OPENAI_API_KEY is not set."
                    )

                client = OpenAI(
                    api_key=api_key
                )

                # -------------------------
                # HOSPITAL DATABASE
                # -------------------------

                hospitals = Hospital.objects.all()

                hospital_data = []

                for hospital in hospitals:

                    hospital_data.append(
                        f"""
Hospital Name: {hospital.name}
City: {hospital.city}
Area: {hospital.area}
Address: {hospital.address}
Facilities: {hospital.facilities}
Emergency Available: {hospital.emergency}
Ambulance Available: {hospital.ambulance}
Rating: {hospital.rating}
"""
                    )

                # -------------------------
                # TREATMENT DATABASE
                # -------------------------

                treatments = Treatment.objects.all()

                treatment_data = []

                for treatment in treatments:

                    treatment_data.append(
                        f"""
Treatment: {treatment.name}
Department: {treatment.department}
Minimum Cost: ₹{treatment.min_cost}
Maximum Cost: ₹{treatment.max_cost}
Patients Treated: {treatment.patients_treated}
Success Rate: {treatment.success_rate}%
"""
                    )

                database_context = f"""
MEDIFIND HOSPITAL DATABASE

{''.join(hospital_data)}


MEDIFIND TREATMENT DATABASE

{''.join(treatment_data)}
"""

                # -------------------------
                # AI REQUEST
                # -------------------------

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    instructions="""

You are the MediFind healthcare assistant.

You are part of a hospital-finder website.

Your responsibilities:

1. Answer general healthcare information questions.

2. If a user describes symptoms,
   explain which type of medical specialist
   or department may be relevant.

3. Give general educational information
   about diseases, symptoms and treatments.

4. Do NOT diagnose the user.

5. Do NOT claim that the user definitely
   has a disease.

6. For severe or potentially emergency symptoms,
   clearly recommend seeking urgent medical care.

7. When the user asks about hospitals,
   treatments, facilities, costs, ratings,
   locations or statistics belonging to MediFind,
   use ONLY the database information supplied below.

8. NEVER invent a hospital name, treatment,
   price, rating, facility or statistic.

9. If information is not present in the database,
   clearly say that it is not currently available
   in the MediFind database.

10. You can still answer general healthcare
    questions using general medical knowledge.

11. Keep responses simple, helpful and easy to understand.

12. Treatment costs and statistics shown by MediFind
    are estimates/demo information and actual medical
    costs and outcomes can vary.

13. For emergency situations, tell the user to seek
    immediate professional medical help.

14. Do not provide a definitive medical diagnosis.

""",

                    input=f"""
Here is the current MediFind database:

{database_context}


USER QUESTION:

{user_message}
"""
                )

                answer = response.output_text

            except Exception as e:

                print(
                    "AI CHATBOT ERROR:",
                    repr(e)
                )

                answer = (
                    "Sorry, I could not connect to "
                    "the AI assistant right now. "
                    "Please try again."
                )

    return render(
        request,
        "hospitals/chatbot.html",
        {
            "answer": answer,
            "user_message": user_message,
        }
    )


# =========================
# CONTACT
# =========================

def contact(request):

    success = False

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        if name and email and subject and message:

            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )

            success = True

    return render(
        request,
        "hospitals/contact.html",
        {
            "success": success
        }
    )