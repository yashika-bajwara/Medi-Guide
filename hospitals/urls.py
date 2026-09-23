from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "hospitals/",
        views.hospital_list,
        name="hospital_list"
    ),

    path(
        "hospital/<int:pk>/",
        views.hospital_detail,
        name="hospital_detail"
    ),

    path(
        "treatments/",
        views.treatments,
        name="treatments"
    ),

    path(
        "analytics/",
        views.analytics,
        name="analytics"
    ),

    path(
        "chatbot/",
        views.chatbot,
        name="chatbot"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),
]