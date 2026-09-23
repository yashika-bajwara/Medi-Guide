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
    hospitals = Hospital.objects.all().order_by("-rating", "name")

    search_query = request.GET.get("q", "").strip()
    selected_city = request.GET.get("city", "").strip()
    selected_budget = request.GET.get("budget", "").strip()
    selected_facility = request.GET.get("facility", "").strip()
    selected_emergency = request.GET.get("emergency", "").strip()

    # Main health-problem / treatment search
    if search_query:
        query = search_query.lower()

        # Common health-problem keywords mapped to treatments/departments
        problem_map = {
            "heart": ["cardiology", "angioplasty", "heart bypass", "pacemaker"],
            "cardiac": ["cardiology", "angioplasty", "heart bypass", "pacemaker"],
            "chest pain": ["cardiology", "angioplasty", "heart bypass"],
            "knee": ["knee replacement", "orthopedics", "fracture"],
            "joint": ["knee replacement", "orthopedics", "physiotherapy"],
            "bone": ["orthopedics", "fracture", "knee replacement"],
            "diabetes": ["diabetes management", "endocrinology"],
            "sugar": ["diabetes management", "endocrinology"],
            "kidney": ["kidney stone treatment"],
            "kidney stone": ["kidney stone treatment"],
            "stone": ["kidney stone treatment"],
            "eye": ["cataract surgery"],
            "cataract": ["cataract surgery"],
            "skin": ["skin allergy treatment", "acne treatment", "dermatology"],
            "acne": ["acne treatment"],
            "fever": ["pediatric fever treatment", "general medicine"],
            "child": ["pediatric fever treatment"],
            "children": ["pediatric fever treatment"],
            "tooth": ["dental root canal", "dental implant"],
            "teeth": ["dental root canal", "dental implant"],
            "dental": ["dental root canal", "dental implant"],
            "breathing": ["asthma management", "pneumonia treatment"],
            "asthma": ["asthma management"],
            "pneumonia": ["pneumonia treatment"],
            "migraine": ["migraine treatment", "neurology"],
            "headache": ["migraine treatment", "neurology"],
            "stroke": ["stroke rehabilitation", "neurology"],
            "thyroid": ["thyroid treatment", "endocrinology"],
            "blood pressure": ["blood pressure management"],
            "bp": ["blood pressure management"],
            "fracture": ["fracture treatment", "orthopedics"],
            "injury": ["fracture treatment", "orthopedics"],
            "appendix": ["appendectomy"],
            "appendicitis": ["appendectomy"],
            "gallbladder": ["gallbladder surgery"],
            "hernia": ["hernia repair"],
            "delivery": ["normal delivery", "cesarean section"],
            "pregnancy": ["normal delivery", "cesarean section"],
            "maternity": ["normal delivery", "cesarean section"],
            "ent": ["ent infection treatment", "tonsil surgery"],
            "ear": ["ent infection treatment"],
            "nose": ["ent infection treatment"],
            "throat": ["ent infection treatment", "tonsil surgery"],
            "mri": ["mri scan"],
            "ct": ["ct scan"],
            "scan": ["mri scan", "ct scan", "ultrasound"],
            "ultrasound": ["ultrasound"],
            "physiotherapy": ["physiotherapy"],
            "therapy": ["physiotherapy"],
        }

        matching_terms = [query]

        for problem, treatments_list in problem_map.items():
            if problem in query:
                matching_terms.extend(treatments_list)

        # Find matching treatments
        treatment_query = models.Q()

        for term in matching_terms:
            treatment_query |= (
                models.Q(name__icontains=term) |
                models.Q(department__icontains=term)
            )

        matching_treatments = Treatment.objects.filter(
            treatment_query
        ).distinct()

        # Find hospitals offering matching treatments
        matching_hospital_ids = HospitalTreatment.objects.filter(
            treatment__in=matching_treatments,
            available=True
        ).values_list("hospital_id", flat=True)

        # Also allow direct hospital/city/facility matching
        hospitals = hospitals.filter(
            models.Q(id__in=matching_hospital_ids) |
            models.Q(name__icontains=query) |
            models.Q(city__icontains=query) |
            models.Q(area__icontains=query) |
            models.Q(facilities__icontains=query) |
            models.Q(description__icontains=query)
        ).distinct()

    # City filter
    if selected_city:
        hospitals = hospitals.filter(city__iexact=selected_city)

    # Facility filter
    if selected_facility:
        hospitals = hospitals.filter(
            facilities__icontains=selected_facility
        )

    # Emergency filter
    if selected_emergency == "true":
        hospitals = hospitals.filter(emergency=True)

    # Budget filter
    if selected_budget:
        try:
            budget = float(selected_budget)

            matching_hospital_ids = HospitalTreatment.objects.filter(
                estimated_cost__lte=budget,
                available=True
            ).values_list("hospital_id", flat=True)

            hospitals = hospitals.filter(
                id__in=matching_hospital_ids
            ).distinct()

        except (ValueError, TypeError):
            pass

    # Cities
    cities = Hospital.objects.values_list(
        "city",
        flat=True
    ).distinct().order_by("city")

    # Facilities
    facilities = set()

    for hospital in Hospital.objects.all():
        if hospital.facilities:
            for facility in hospital.facilities.split(","):
                facility = facility.strip()
                if facility:
                    facilities.add(facility)

    facilities = sorted(facilities)

    context = {
        "hospitals": hospitals,
        "cities": cities,
        "facilities": facilities,
        "search_query": search_query,
        "selected_city": selected_city,
        "selected_budget": selected_budget,
        "selected_facility": selected_facility,
        "selected_emergency": selected_emergency,
    }

    return render(
        request,
        "hospitals/hospitals.html",
        context
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