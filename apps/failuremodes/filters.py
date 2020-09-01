from django.core.paginator import Paginator
from .models import FailureMode


def failuremode_filter(query_params={}):
    queryset = FailureMode.objects.order_by('-code')

    if 'q' in query_params:
        query = query_params['q']
        queryset = queryset.filter(name__icontains=query, )

    elif 'subsystem' in query_params:
        query = query_params['subsystem']
        queryset = queryset.filter(component__subsystem=query, )

    paginator = Paginator(queryset, 15)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings