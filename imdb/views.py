import json
import pdb
import sys
import traceback

import requests

import SearchResults


from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def search_movie(request):

    movie = request.GET.get('q', '')
    error, status, movie_list = SearchResults.get_search_movies(movie)

    if error:
        data = json.dumps(movie_list)
        return HttpResponse(data,
                            content_type='application/json',
                            status=status)
    paginator = Paginator(movie_list, 15)
    page = request.GET.get(page)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(1)

    movies = movies.object_list
    data = json.dumps(movies)

    return HttpResponse(data,
                        content_type='application/json',
                        status=status)


def exact_match(request, movie_id):
    error, status, data = SearchResults.get_movie_results(movie_id)

    data =json.dumps(data)
    return HttpResponse(data,
                        content_type='application/json',
                        status = status)



