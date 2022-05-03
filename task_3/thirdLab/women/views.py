from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = ["About", "Add article", "Feedback", "Log In"]


def index(request):
    posts = Women.objects.all()
    return render(request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Main page'})


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'About'})


def categories(request, cat_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Articles by categories</h1><p>{cat_id}</p>")


def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)

    return HttpResponse(f"<h1>Archive by years</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')
