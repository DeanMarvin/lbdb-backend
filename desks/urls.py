from django.urls import path

from desks.views import (
    get_available_desks,
    get_available_desks_update,
    update_desk,
    get_available_desks_turnus,
    get_unavailable_desks,
)

urlpatterns = [
    path("available/", get_available_desks),
    path("available/turnus/", get_available_desks_turnus),
    path("available/reservation/", get_available_desks_update),
    path("unavailable/", get_unavailable_desks),
    path("update/", update_desk),
]
