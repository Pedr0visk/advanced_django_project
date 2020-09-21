from django.shortcuts import render

from apps.bops.models import Bop


def certification_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)
    certifications = bop.certifications.all()

    context = {'bop': bop, 'certifications': certifications}
    return render(request, 'certifications/certification_list.html', context)
