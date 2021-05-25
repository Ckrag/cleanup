import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render

from public.models import CleanNode, CleanRoute


def index(request: HttpRequest):
    context = {
        "routes": CleanRoute.objects.order_by('-pub_date')[:10]
    }
    return render(request, 'public/index.html', context)


def get_map_relevant_nodes(request: HttpRequest):
    if request.method != "POST":
        return Http404()
    data = json.loads(request.body)
    lat = data['lat']
    lng = data['lng']
    lng_delta = data['lng_delta']
    lat_delta = data['lat_delta']

    query = CleanNode.objects.filter(
        decay_date__lte=datetime.date.today(),
        lat__lte=lat,
        lat__gte=lat - lat_delta,
        lng__gte=lng,
        lng__lte=lng + lng_delta
    )
    query = query.select_related('route').only('route__title', 'route__id')
    query = query.select_related('author').only('author__username')
    query = query.annotate(
        author_username=F('author__username'),
        route_title=F('route__title'),
    )
    nodes = list(query.values(
        'id', 'lat', 'lng', 'author_username', 'route_title', 'route_id'
    ))
    return JsonResponse({
        "nodes": nodes
    })


@login_required
def contribute(request: HttpRequest):
    if request.method == "POST":
        contr = json.loads(request.body)

        if len(contr['path']) == 0:
            return JsonResponse({}, status=400)
        if 'title' not in contr or len(contr['title'].strip()) == 0:
            return JsonResponse({}, status=400)
        if 'description' not in contr or len(contr['description'].strip()) == 0:
            return JsonResponse({}, status=400)

        route = CleanRoute()
        route.title = contr['title']
        route.description = contr['description']
        route.decay_date = '2021-05-19 21:38:25+00'
        route.pub_date = '2021-05-19 21:38:25+00'
        route.author = request.user
        route.save()

        for node in contr['path']:
            lat = node[0]
            lng = node[1]
            clean_node = CleanNode()
            clean_node.lat = lat
            clean_node.lng = lng
            clean_node.route = route
            clean_node.author = request.user
            clean_node.decay_date = '2021-05-19 21:38:25+00'
            clean_node.pub_date = '2021-05-19 21:38:25+00'
            clean_node.save()

        return JsonResponse({
            "status": "accepted"
        }, status=201)
    else:
        return render(request, 'public/contribute.html', {})


def contribution(request: HttpRequest, route_id: int):
    routes = CleanRoute.objects.filter(id=route_id)
    routes = routes.select_related('author').only('author__username')
    routes = routes.annotate(
        author_username=F('author__username'),
    )
    return render(request, 'public/contribution.html', {
        "route": routes[0]
    })
