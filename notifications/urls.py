from django.urls import path

from notifications.views import get_notifications, update_notifications

urlpatterns = [
    path('current/', get_notifications),
    path('update/', update_notifications)
]
