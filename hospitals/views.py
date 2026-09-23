import os
import requests

from django.shortcuts import render, get_object_or_404
from django.db import models

from .models import (
    Hospital,
    Treatment,
    HospitalTreatment,
    ContactMessage,
)


# ============================================================
# HOME
# ============================================================

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


# ============================================================
# HOSPITAL LIST
# ============================================================

def hospital_list(request):

    hospitals = Hospital.objects.all()

    query = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    budget = request.GET.get("budget", "").strip()
    facility = request.GET.get("facility", "").strip()
    emergency = request.GET.get("emergency", "").strip()

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

    if city:
        hospitals = hospitals.filter(
            city__icontains=city
        )

    if budget:
        try:
            hospitals = hospitals.filter(
                hospitaltreatment__estimated_cost__lte=float(budget)
            )
        except (ValueError, TypeError):
            pass

    if facility:
        hospitals = hospitals.filter(
            facilities__icontains=facility
        )

    if emergency == "true":
        hospitals = hospitals.filter(
            emergency=True
        )

    hospitals = hospitals.distinct()

    cities = (
        Hospital.objects
        .values_list("city", flat=True)
        .distinct()
        .order_by("city")
    )

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


# ============================================================
# HOSPITAL DETAIL
# ============================================================

def hospital_detail(request, pk):

    hospital = get_object_or_404(
        Hospital,
        pk=pk
    )

    treatments = (
        HospitalTreatment.objects
        .filter(
            hospital=hospital,
            available=True
        )
        .select_related("treatment")
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


# ============================================================
# TREATMENTS
# ============================================================

def treatments(request):

    treatment_list = (
        Treatment.objects
        .all()
        .order_by("name")
    )

    query = request.GET.get("q", "").strip()
    department = request.GET.get("department", "").strip()

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


# ============================================================
# ANALYTICS
# ============================================================

def analytics(request):

    treatments = Treatment.objects.all()

    total_patients = sum(
        treatment.patients_treated
        for treatment in treatments
    )

    if treatments.exists():

        average_success_rate = (
            sum(
                float(treatment.success_rate)
                for treatment in treatments
            )
            / treatments.count()
        )

        average_budget = (
            sum(
                (
                    float(treatment.min_cost)
                    + float(treatment.max_cost)
                ) / 2
                for treatment in treatments
            )
            / treatments.count()
        )

    else:

        average_success_rate = 0
        average_budget = 0

    return render(
        request,
        "hospitals/analytics.html",
        {
            "total_patients": total_patients,
            "average_success_rate": round(
                average_success_rate,
                2
            ),
            "average_budget": round(
                average_budget,
                2
            ),
            "treatments": treatments,
        }
    )


# ============================================================
# GEMINI AI CHATBOT
# ============================================================

def chatbot(request):

    answer = None
    user_message = None

    if request.method == "POST":

        user_message = request.POST.get(
            "message",
            ""
        ).strip()

        if user_message:

            # ------------------------------------------------
            # GET HOSPITAL DATA FROM DATABASE
            # ------------------------------------------------

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
Emergency Service: {"Yes" if hospital.emergency else "No"}
Ambulance: {"Yes" if hospital.ambulance else "No"}
Rating: {hospital.rating}
Description: {hospital.description}
"""
                )

            # ------------------------------------------------
            # GET TREATMENT DATA FROM DATABASE
            # ------------------------------------------------

            treatments = Treatment.objects.all()

            treatment_data = []

            for treatment in treatments:

                average_cost = (
                    float(treatment.min_cost)
                    + float(treatment.max_cost)
                ) / 2

                treatment_data.append(
                    f"""
Treatment: {treatment.name}
Department: {treatment.department}
Minimum Cost: ₹{treatment.min_cost}
Maximum Cost: ₹{treatment.max_cost}
Average Estimated Cost: ₹{average_cost:.2f}
Patients Treated: {treatment.patients_treated}
Success Rate: {treatment.success_rate}%
Description: {treatment.description}
"""
                )

            # ------------------------------------------------
            # COMPLETE AI INSTRUCTION
            # ------------------------------------------------

            website_context = f"""
You are MediFind Assistant, the AI healthcare assistant
for the MediFind hospital finder website.

Your job is to help users with:

1. Hospitals
2. Treatments
3. Treatment costs
4. Hospital locations
5. Hospital facilities
6. Emergency services
7. Ambulance availability
8. Hospital ratings
9. General healthcare questions
10. General medical information
11. Questions about how to use MediFind

IMPORTANT RULES:

- Be friendly, clear and helpful.
- Answer general questions normally.
- For MediFind-specific questions, use the database information
  provided below.
- Do NOT invent hospitals, treatments, prices, facilities,
  ratings or statistics.
- The hospital and treatment information below is
  DEMO/SAMPLE data for this website.
- If the requested information is not present in the database,
  clearly say that it is not currently available in MediFind.
- For medical questions, provide general educational information.
- Do not diagnose users.
- Do not claim to replace a doctor.
- If a user describes a serious emergency, advise them to contact
  local emergency services or seek immediate professional care.
- Keep normal answers reasonably concise.
- Use bullet points when they make the answer easier to read.
- If the user asks about a specific hospital, give the relevant
  information about that hospital.
- If the user asks about treatment cost, clearly mention that
  these are estimated/sample website values.
- If the user asks for hospitals in a city, list matching hospitals
  from the database.

==================================================
MEDIFIND HOSPITAL DATABASE
==================================================

{chr(10).join(hospital_data)}

==================================================
MEDIFIND TREATMENT DATABASE
==================================================

{chr(10).join(treatment_data)}

==================================================
USER QUESTION
==================================================

{user_message}
"""

            # ------------------------------------------------
            # GET GEMINI API KEY
            # ------------------------------------------------

            api_key = os.environ.get(
                "GEMINI_API_KEY"
            )

            if not api_key:

                answer = (
                    "The AI assistant is not configured yet. "
                    "Please contact the website administrator."
                )

            else:

                try:

                    # ----------------------------------------
                    # GEMINI API
                    # ----------------------------------------

                    url = (
                        "https://generativelanguage.googleapis.com/"
                        "v1beta/models/"
                        "gemini-3.5-flash-lite:"
                        "generateContent"
                    )

                    headers = {
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    }

                    payload = {
                        "contents": [
                            {
                                "parts": [
                                    {
                                        "text": website_context
                                    }
                                ]
                            }
                        ]
                    }

                    response = requests.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )

                    data = response.json()

                    # ----------------------------------------
                    # SUCCESS
                    # ----------------------------------------

                    if response.status_code == 200:

                        candidates = data.get(
                            "candidates",
                            []
                        )

                        if candidates:

                            parts = (
                                candidates[0]
                                .get("content", {})
                                .get("parts", [])
                            )

                            if parts:

                                answer = parts[0].get(
                                    "text",
                                    "Sorry, I could not generate an answer."
                                )

                            else:

                                answer = (
                                    "Sorry, I could not generate "
                                    "an answer right now."
                                )

                        else:

                            answer = (
                                "Sorry, I could not generate "
                                "an answer right now."
                            )

                    # ----------------------------------------
                    # API ERROR
                    # ----------------------------------------

                    else:

                        answer = (
                            "Sorry, the AI assistant is temporarily "
                            "unavailable. Please try again."
                        )

                        print(
                            "Gemini API Error:",
                            response.status_code,
                            data
                        )

                # --------------------------------------------
                # TIMEOUT
                # --------------------------------------------

                except requests.exceptions.Timeout:

                    answer = (
                        "The AI assistant took too long to respond. "
                        "Please try again."
                    )

                # --------------------------------------------
                # CONNECTION ERROR
                # --------------------------------------------

                except requests.exceptions.ConnectionError:

                    answer = (
                        "I could not connect to the AI assistant. "
                        "Please check your internet connection "
                        "and try again."
                    )

                # --------------------------------------------
                # OTHER ERROR
                # --------------------------------------------

                except Exception as e:

                    print(
                        "Chatbot Error:",
                        str(e)
                    )

                    answer = (
                        "Sorry, I could not connect to the "
                        "AI assistant right now. Please try again."
                    )

    return render(
        request,
        "hospitals/chatbot.html",
        {
            "user_message": user_message,
            "answer": answer,
        }
    )


# ============================================================
# CONTACT
# ============================================================

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
                message=message
            )

            success = True

    return render(
        request,
        "hospitals/contact.html",
        {
            "success": success
        }
    )