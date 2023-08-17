from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from staff.models import Staff
from .models import Notifications
from .serializer import NotificationSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request, *args, **kwargs):

    s_id = Staff.objects.get(user=request.user.id)

    start_date = datetime.date(datetime.today())
    end_date = start_date - timedelta(days=14)

    notifications_checked = Notifications.objects.filter(datum__gte=end_date, datum__lte=start_date, s_id=s_id, checked=True).order_by('-datum')
    notifications_checked_serializer = NotificationSerializer(notifications_checked, many=True)

    notifications_unchecked = Notifications.objects.filter(datum__gte=end_date, datum__lte=start_date, s_id=s_id, checked=False).order_by('-datum')
    notifications_unchecked_serializer = NotificationSerializer(notifications_unchecked, many=True)

    notification_new = Notifications.objects.filter(datum__gte=end_date, datum__lte=start_date, s_id=s_id, checked=False).count()

    return Response(
        { "checked" : notifications_checked_serializer.data[:10], "unchecked" : notifications_unchecked_serializer.data, "new" : notification_new }, status=200)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_notifications(request, *args, **kwargs):

    s_id = Staff.objects.get(user=request.user.id)

    for i in request.data:
        serializer = NotificationSerializer(data=i)

        if serializer.is_valid(raise_exception=True):
            Notifications.objects.filter(s_id=s_id, datum=serializer.data['datum']).update(checked=True)

    return Response(status=201)

def delete_outdated_notifications(request, *args, **kwargs):

    users = Staff.objects.filter(aktiv=True)
    date = datetime.date(datetime.today() - timedelta(days=14))

    for user in users:
        outdated_notifications = Notifications.objects.filter(s_id=user.s_id, datum__lte=date)
        for outdated in outdated_notifications:
            outdated.delete()