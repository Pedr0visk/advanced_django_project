from rest_framework import viewsets
from .serializers import TestScheduleSerializer, TestGroupSerializer
from apps.test_groups.models import TestGroup, TestSchedule


class TestGroupViewSet(viewsets.ModelViewSet):
    queryset = TestGroup.objects.all()
    serializer_class = TestGroupSerializer


class TestScheduleViewSet(viewsets.ModelViewSet):
    queryset = TestSchedule.objects.all()
    serializer_class = TestScheduleSerializer
