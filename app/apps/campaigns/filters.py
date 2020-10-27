from django.core.paginator import Paginator
from django.db.models import Q


def campaign_filter(data_set, query_params={}):
    if 'q' in query_params:
        query = query_params['q']
        data_set = data_set.filter(Q(name__icontains=query))

    elif 'bop' in query_params:
        query = query_params['subsystem']
        data_set = data_set.filter(component__subsystem=query, )

    elif 'component' in query_params:
        query = query_params['component']
        data_set = data_set.filter(component=query, )

    paginator = Paginator(data_set, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
