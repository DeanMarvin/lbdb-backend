from rest_framework import serializers

from .models import Motions

class MotionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Motions
        fields = ['startdatum', 'enddatum', 'antragsteller_vorname', 'antragsteller_nachname', 'antragsteller_initialen']