from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CertificationForm
from .models import Certification
from ..bops.models import Bop
from django.core.cache import cache


def certification_list(request, bop_pk):
    bop = Bop.objects.get(pk=bop_pk)

    certifications = bop.certifications.all()

    context = {'bop': bop, 'objects': certifications}
    return render(request, 'certifications/certification_list.html', context)


def certification_update(request, bop_pk, cert_pk):
    bop = Bop.objects.get(pk=bop_pk)
    certification = Certification.objects.get(pk=cert_pk)
    form = CertificationForm(request.POST or None, instance=certification)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Certification "{certification.code}" successfully updated!')
            return redirect('list_certifications', bop_pk)

    context = {'form': form, 'bop': bop, 'object': certification}
    return render(request, 'certifications/certification_form.html', context)
