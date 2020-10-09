from rest_framework import viewsets
from .serializers import TestGroupSerializer
from apps.test_groups.models import TestGroup


class TestGroupViewSet(viewsets.ModelViewSet):
    queryset = TestGroup.objects.all()
    serializer_class = TestGroupSerializer
