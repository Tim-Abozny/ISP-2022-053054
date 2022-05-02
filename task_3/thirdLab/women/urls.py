from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index),    # http://127.0.0.1:8000/
    path('cats/<int:cat_id>/', categories),  # http://127.0.0.1:8000/cats/
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]