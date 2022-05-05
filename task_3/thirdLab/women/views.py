from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [
    {'title': "About", 'url_name': 'about'},
    {'title': "Add article", 'url_name': 'add_page'},
    {'title': "Feedback", 'url_name': 'contact'},
    {'title': "Log In", 'url_name': 'login'}
]


def index(request):
    posts = Women.objects.all()
    cats = Category.objects.all()

    send_parameters = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Main page',
        'cat_selected': 0
    }
    return render(request, 'women/index.html', context=send_parameters)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'About'})


def addpage(request):
    return HttpResponse("Add article")


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Authorization")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')


def show_post(request, post_id):
    return HttpResponse(f"Show article with id = {post_id}")


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404

    send_parameters = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Display by category',
        'cat_selected': cat_id
    }
    return render(request, 'women/index.html', context=send_parameters)
