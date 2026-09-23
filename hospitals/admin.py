from django.contrib import admin
from .models import (
    Hospital,
    Treatment,
    HospitalTreatment,
    Review,
    ContactMessage,
)


# =========================================================
# HOSPITAL
# =========================================================

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "city",
        "area",
        "phone",
        "emergency",
        "ambulance",
        "rating",
    )

    list_filter = (
        "city",
        "emergency",
        "ambulance",
    )

    search_fields = (
        "name",
        "city",
        "area",
        "address",
        "phone",
    )
# =========================================================
# TREATMENT
# =========================================================

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "department",
        "min_cost",
        "max_cost",
        "patients_treated",
        "success_rate",
    )

    list_filter = (
        "department",
    )

    search_fields = (
        "name",
        "department",
    )


# =========================================================
# HOSPITAL TREATMENT
# =========================================================

@admin.register(HospitalTreatment)
class HospitalTreatmentAdmin(admin.ModelAdmin):

    list_display = (
        "hospital",
        "treatment",
        "estimated_cost",
        "available",
    )

    list_filter = (
        "available",
        "treatment",
    )

    search_fields = (
        "hospital__name",
        "treatment__name",
    )


# =========================================================
# REVIEWS
# =========================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "hospital",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
        "hospital",
    )

    search_fields = (
        "name",
        "hospital__name",
        "comment",
    )


# =========================================================
# CONTACT MESSAGES
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    list_filter = (
        "created_at",
    )