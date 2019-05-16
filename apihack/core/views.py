from django.apps import apps
from django.http import HttpResponse
from django.core.serializers import serialize
from collections import namedtuple
import asyncio


def home(request, app, model, pk=None):
    opcoes = verifica_opcoes(request, app, model, pk)
    return HttpResponse(serialize(opcoes.fmt, opcoes.qs), content_type=f'application/{opcoes.fmt}')


def verifica_opcoes(request, app, model, pk):
    model = apps.get_model(f'{app}.{model}')
    qs = model.objects.all()

    rel = request.GET.get('rel', None)
    fmt = request.GET.get('fmt', 'json')

    if pk:
        qs = qs.filter(pk=pk)

    if rel:
        related = rel.split(',')
        qs = qs.select_related(*related)

    opcoes = namedtuple('Opcoes', ['fmt', 'qs'])

    return opcoes(fmt, qs)
