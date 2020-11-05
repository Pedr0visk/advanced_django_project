from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.bops.models import Bop
from .serializers import BopSerializer
from apps.test_groups.api.serializers import TestGroupSerializer
from rest_framework import status


class BopViewSet(viewsets.ModelViewSet):
    queryset = Bop.objects.all()
    serializer_class = BopSerializer

    def retrieve(self, request, pk=None):
        bop = get_object_or_404(self.queryset, pk=pk)
        serializer = BopSerializer(bop)
        data = serializer.data
        last_certification = bop.last_certification()
        data['last_certification'] = {'end_date': last_certification.end_date}
        return Response(data)

    @action(methods=['get'], detail=True, url_path='test-groups')
    def list_test_groups(self, request, pk=None):
        try:
            bop = Bop.objects.get(pk=pk)
        except Bop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            test_groups = bop.testgroup.all()
            serializer = TestGroupSerializer(test_groups, many=True)
            return Response(serializer.data)
