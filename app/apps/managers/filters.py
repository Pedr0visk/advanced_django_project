import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.models import User


class AccountFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['username']


def account_filter(query_params={}):
    accounts = User.objects.order_by('-username')

    if 'username' in query_params:
        username = query_params['username']

        accounts = accounts.filter(username__icontains=username)

    paginator = Paginator(accounts, 2)
    page = query_params.get('page')
    paged_listings = paginator.get_page(page)

    return paged_listings


