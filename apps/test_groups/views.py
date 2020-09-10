from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import TestGroupForm
from ..bops.models import Bop
from ..failuremodes.models import FailureMode
from ..tests.models import Test


def test_group_list(request):
    return HttpResponse('test group list')


def test_group_create(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    form = TestGroupForm(request.POST or None)
    test_set = Test.objects.all()
    failure_mode_set = FailureMode.objects.order_by('name')

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_test_groups', bop_pk)

    context = {'form': form, 'bop': bop, 'tests': test_set, 'failure_modes': failure_mode_set}
    return render(request, 'test_groups/test_group_form.html', context)
