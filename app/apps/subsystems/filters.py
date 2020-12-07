from django.core.paginator import Paginator
from django.db.models import Q
from .models import Subsystem


def subsystem_filter(query_params={}):
    queryset = Subsystem.objects.prefetch_related('bop').order_by('name')

    if 'q' in query_params:
        query = query_params['q']
        if len(query) > 0:
            queryset = queryset.filter(Q(name__icontains=query) | Q(code__icontains=query))

    if 'bop' in query_params:
        query = query_params['bop']
        queryset = queryset.filter(bop_id=query)

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
