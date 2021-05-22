# Create your views here.
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from public.models import CleanNode, CleanRoute


def index(request: HttpRequest):
    context = {
        "grouped_nodes": CleanNode.objects.order_by('-pub_date')
    }
    return render(request, 'public/index.html', context)


@login_required
def contribution(request: HttpRequest):
    if request.method == "POST":
        contr = json.loads(request.body)

        if len(contr['path']) == 0:
            return JsonResponse({}, status=400)

        route = CleanRoute()
        route.title = contr['name']
        route.description = "my description"
        route.decay_date = '2021-05-19 21:38:25+00'
        route.pub_date = '2021-05-19 21:38:25+00'
        route.author = request.user
        route.save()

        for node in contr['path']:
            lat = node[0]
            lng = node[1]
            clean_node = CleanNode()
            clean_node.lat = lat
            clean_node.lon = lng
            clean_node.route = route
            clean_node.author = request.user
            clean_node.decay_date = '2021-05-19 21:38:25+00'
            clean_node.pub_date = '2021-05-19 21:38:25+00'
            clean_node.save()

        return JsonResponse({
            "status": "accepted"
        }, status=201)
    else:
        return render(request, 'public/contribution.html', {})
