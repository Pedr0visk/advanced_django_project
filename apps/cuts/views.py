from django.http.response import HttpResponse
from django.shortcuts import render
from .filters import cut_filter


def cut_list(request):
    cuts = cut_filter(request.GET)

    context = {'cuts': cuts}
    return render(request, 'cuts/cut_list.html', context)
