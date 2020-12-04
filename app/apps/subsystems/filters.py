from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Subsystem


def subsystem_filter(query_params={}):
    queryset = Subsystem.objects.prefetch_related('bop').order_by('name')

    if 'q' in query_params:
        query = query_params['q']
        queryset = queryset.filter(name__icontains=query)

    if 'bop' in query_params:
        query = query_params['bop']
        queryset = queryset.filter(bop_id=query)

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
