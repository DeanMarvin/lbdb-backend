from django.urls import path

from motions.views import (
    unhandled_vacation_motions,
    overlapping_vacations,
    confirm_vacation,
    reject_vacation,
)

urlpatterns = [
    path("check/", overlapping_vacations),
    path("confirm/", confirm_vacation),
    path("current/", unhandled_vacation_motions),
    path("reject/", reject_vacation),
]
