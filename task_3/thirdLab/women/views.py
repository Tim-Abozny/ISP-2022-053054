from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render


def index(request):
    return HttpResponse("Women application page")


def categories(request, cat_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Articles by categories</h1><p>{cat_id}</p>")


def archive(request, year):
    if int(year) > 2022:
        raise Http404()

    return HttpResponse(f"<h1>Archive by years</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')
