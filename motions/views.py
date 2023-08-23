from datetime import datetime, timedelta, date

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Motions
from .serializer import MotionsSerializer

from desks.models import Desks
from notifications.models import Notifications
from staff.models import Staff
from workingdays.holidays import bavarian_holidays
from workingdays.models import Workingdays, Status


# get vacation status_id with default No. 3.
vacation_status_id = Status.objects.get(status_id=3)


def get_vacation_days(vacation):
    # get the amount of vacation days by user motion.

    result = []
    day_counter = 0
    for vacation_day in vacation:
        start_date = vacation_day.startdatum
        end_date = vacation_day.enddatum
        days_dict = {"days": 0}
        while start_date <= end_date:
            if start_date.isoweekday() <= 5:
                if not bavarian_holidays(start_date):
                    day_counter += 1
            start_date += timedelta(days=1)
        days_dict["days"] = day_counter
        result.append(days_dict)
    return result


def get_vacation_days_left(vacation):
    # get the amount of vacation days left.

    result = []
    for i in vacation:
        initialen = i.antragsteller_initialen
        last_name = i.antragsteller_nachname
        user = Staff.objects.filter(initialen=initialen, nachname=last_name).values(
            "urlaubstage_total", "urlaubstage_genommen"
        )
        vacation_days_left = (
            user[0]["urlaubstage_total"] - user[0]["urlaubstage_genommen"]
        )
        left_dict = {"left": vacation_days_left}
        result.append(left_dict)
    return result


def get_overlapping_vacations(start_date, end_date):
    # get overlapping results

    result = []
    overlapping_vacations = Workingdays.objects.filter(
        datum__gte=start_date, datum__lte=end_date, status_id=vacation_status_id
    ).values("s_id")

    for user in overlapping_vacations:
        employee = Staff.objects.filter(s_id=user["s_id"]).values(
            "vorname", "nachname", "initialen"
        )
        if employee[0] not in result:
            result.append(employee[0])
    return result


def create_vacation_day(user, user_id, start_date, end_date):
    # create vacation day after confirmation.

    stunden = user[0].wochenstunden / user[0].wochenarbeitstage
    desk_id = Desks.objects.get(d_id=999)

    while start_date <= end_date:
        workingday = Workingdays.objects.filter(datum=start_date, s_id__in=user)

        if not bavarian_holidays(start_date):
            if start_date.isoweekday() <= 5:
                if not workingday.exists():
                    new_vacation_day = Workingdays.objects.create(
                        datum=start_date,
                        s_id=user_id,
                        status_id=vacation_status_id,
                        sollstunden=stunden,
                        iststunden=stunden,
                        d_id=desk_id,
                        erstellt=datetime.now(),
                    )
                    new_vacation_day.save()
                else:
                    workingday.update(
                        status_id=vacation_status_id,
                        sollstunden=stunden,
                        iststunden=stunden,
                        d_id=desk_id,
                    )
        start_date += timedelta(days=1)


def update_motion(start_date, end_date, initialen):
    # update motion is checked.

    Motions.objects.filter(
        startdatum=start_date,
        enddatum=end_date,
        antragsteller_initialen=initialen,
    ).update(edited=True)


def create_notification(id, type, description):
    Notifications.objects.create(
        s_id=id,
        datum=date.today(),
        type=type,
        description=description,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unhandled_vacation_motions(request, *args, **kwargs):
    s_id = Staff.objects.get(user=request.user.id)

    unhandled = Motions.objects.filter(bearbeiter=s_id, edited=False).order_by(
        "startdatum"
    )
    # count amount of motions
    unhandled_count = Motions.objects.filter(bearbeiter=s_id, edited=False).count()
    # days of vacation
    vacation_days = get_vacation_days(unhandled)
    # get vacation days left
    vacation_days_left = get_vacation_days_left(unhandled)
    # serialized motions
    motion_serializer = MotionsSerializer(unhandled, many=True)

    return Response(
        {
            "motions": motion_serializer.data,
            "motions_count": unhandled_count,
            "vacation_days": vacation_days,
            "vacation_left": vacation_days_left,
        },
        status=200,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def overlapping_vacations(request, *args, **kwargs):
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")
    overlapping = get_overlapping_vacations(start_date, end_date)

    return Response(overlapping, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_vacation(request, *args, **kwargs):
    data = request.data.get("data")
    first_name = data["firstName"]
    last_name = data["lastName"]
    initialen = data["init"]
    vacation_days = data["days"]
    start_date = datetime.date(datetime.strptime(data["startDate"], "%Y-%m-%d"))
    end_date = datetime.date(datetime.strptime(data["endDate"], "%Y-%m-%d"))

    user = Staff.objects.filter(
        initialen=initialen, nachname=last_name, vorname=first_name
    )
    user_id = Staff.objects.get(s_id=user[0].s_id)

    if user:
        create_vacation_day(user, user_id, start_date, end_date)

        # update taken vacation days.
        Staff.objects.filter(
            initialen=initialen, nachname=last_name, vorname=first_name
        ).update(urlaubstage_genommen=user[0].urlaubstage_genommen + vacation_days)

        update_motion(
            start_date=data["startDate"], end_date=data["endDate"], initialen=initialen
        )

        create_notification(
            id=user_id, type="confirmed", description="Urlaubsantrag wurde genehmigt."
        )

        return Response(status=201)

    return Response(status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_vacation(request, *args, **kwargs):
    data = request.data.get("data")
    first_name = data["firstName"]
    last_name = data["lastName"]
    initialen = data["init"]

    staff = Staff.objects.filter(
        initialen=initialen, nachname=last_name, vorname=first_name
    )
    staff_id = Staff.objects.get(s_id=staff[0].s_id)

    update_motion(data["startDate"], data["endDate"], initialen)

    create_notification(
        id=staff_id, type="rejected", description="Urlaubsantrag wurde abgelehnt."
    )

    return Response(status=201)
