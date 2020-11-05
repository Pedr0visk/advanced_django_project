from rest_framework import serializers
from apps.bops.models import Bop


class BopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bop
        fields = (
            'name',
            'model',
        )

