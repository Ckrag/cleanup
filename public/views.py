# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404
from django.shortcuts import render

from public.models import CleanNode


def index(request: HttpRequest):
    context = {
        "grouped_nodes": CleanNode.objects.order_by('-pub_date')
    }
    return render(request, 'public/index.html', context)


def contribution(request: HttpRequest):
    return render(request, 'public/contribution.html', {})


@login_required
def create_contribution(request: HttpRequest):
    if request.method == "POST":
        data = json.loads(request.body)
    else:
        raise Http404()
