from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Subsystem


def subsystem_filter(query_params={}):
    if 'q' in query_params:
        query = query_params['q']

        queryset = Subsystem.objects.filter(name__icontains=query)
    else:
        queryset = Subsystem.objects.all()

    paginator = Paginator(queryset, 10)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings
