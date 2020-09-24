import django_filters

from django.core.paginator import Paginator
from .models import FailureMode


class FailureModeFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = FailureMode
        fields = ['code', 'name']


def failuremode_filter(query_params={}):
    queryset = FailureMode.objects.order_by('-code')

    if 'q' in query_params:
        query = query_params['q']
        queryset = queryset.filter(name__icontains=query, )

    elif 'subsystem' in query_params:
        query = query_params['subsystem']
        queryset = queryset.filter(component__subsystem=query, )

    elif 'component' in query_params:
        query = query_params['component']
        queryset = queryset.filter(component=query, )

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
