from django.core.paginator import Paginator
from .models import Cut


def cut_filter(query_params={}):
    queryset = Cut.objects.order_by('index')

    if 'sf' in query_params:
        query = query_params['sf']
        queryset = queryset.filter(safety_function=query, )

    if 'order' in query_params:
        query = query_params['order']
        queryset = queryset.filter(order=query, )

    paginator = Paginator(queryset, 25)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
