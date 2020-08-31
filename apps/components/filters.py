from django.core.paginator import Paginator
from .models import Component


def component_filter(query_params={}):
    if 'q' in query_params:
        query = query_params['q']

        queryset = Component.objects.filter(name__icontains=query,)
    else:
        queryset = Component.objects.all()

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
