from django.core.paginator import Paginator
from django.db.models import Q
from .models import Component


def component_filter(query_params={}):
    queryset = Component.objects.prefetch_related('subsystem').order_by('name')

    if 'q' in query_params:
        query = query_params['q']
        if len(query) > 0:
            queryset = queryset.filter(Q(name__icontains=query) | Q(code__icontains=query))

    if 'bop' in query_params:
        query = query_params['bop']
        if len(query) > 0:
            queryset = queryset.filter(subsystem__bop=query, )

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
