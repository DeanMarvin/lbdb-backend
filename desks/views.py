from desks.models import Desks

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from workingdays.converters import (
    date_to_datetime,
    filter_available_desks_by_date,
    filter_available_with_current_desk,
    filter_available_desks_by_date_active,
    filter_unavailable_desks_by_date,
)
from desks.serializers import DeskSerializer, DeskUpdateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_available_desks(request, *args, **kwargs):
    dates = request.GET
    start_date = dates.get("sd")
    end_date = dates.get("ed")
    start_date, end_date = date_to_datetime(start_date, end_date)
    desks = filter_available_desks_by_date(start_date, end_date)
    serializer = DeskSerializer(desks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unavailable_desks(request, *args, **kwargs):
    dates = request.GET
    start_date = dates.get("sd")
    end_date = dates.get("ed")
    start_date, end_date = date_to_datetime(start_date, end_date)
    desks = filter_unavailable_desks_by_date(start_date, end_date)
    serializer = DeskSerializer(desks, many=True)

    return Response(serializer.data, status=201)


@api_view(["GET"])
def get_available_desks_update(request, *args, **kwargs):
    data = request.GET
    start_date = data.get("sd")
    end_date = data.get("ed")
    desk_id = data.get("d_id")
    start_date, end_date = date_to_datetime(start_date, end_date)
    desks = filter_available_with_current_desk(start_date, end_date, desk_id)
    serializer = DeskSerializer(desks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_available_desks_turnus(request, *args, **kwargs):
    dates = request.GET
    start_date = dates.get("sd")
    end_date = dates.get("ed")
    start_date, end_date = date_to_datetime(start_date, end_date)
    desks = filter_available_desks_by_date_active(start_date, end_date)
    serializer = DeskSerializer(desks, many=True)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_desk(request, *args, **kwargs):
    serializer = DeskUpdateSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        desk_to_update = Desks.objects.get(pk=serializer.data["d_id"])
        desk_to_update.name = serializer.data["name"]
        desk_to_update.client = serializer.data["client"]
        desk_to_update.licence = serializer.data["licence"]
        desk_to_update.active = serializer.data["active"]
        desk_to_update.save()

        return Response(serializer.data, status=201)

    return Response(serializer.data, status=400)
