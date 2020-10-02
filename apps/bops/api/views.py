from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.bops.models import Bop
from .serializers import BopSerializer
from rest_framework import status


class BopViewSet(viewsets.ModelViewSet):
    queryset = Bop.objects.all()
    serializer_class = BopSerializer

    @action(methods=['get'], detail=True, url_path='test-groups')
    def list_test_groups(self, request, pk=None):
        try:
            bop = Bop.objects.get(pk=pk)
        except Bop.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BopSerializer(bop)
            return Response(serializer.data)
