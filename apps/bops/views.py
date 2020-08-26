from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Bop, SafetyFunction, Component, FailureMode, Cut
from .forms import BopForm

from apps.campaigns.forms import CampaignForm


def upload(request):
    form = BopForm()
    context = {'form': form}

    return render(request, 'bops/bop_form.html', context)
