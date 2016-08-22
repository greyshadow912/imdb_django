import logging
import sys
import traceback

import requests

from bs4 import BeautifulSoup


def get_search_movies(movie):

    url = 'http://imdb.com/find' + movie

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.info(e)
        traceback.print_exc(e)
        json_object = {}
        json_object['error'] ="Service Unavailable"
        tup = (True, 503, json_object)
        return tup

    soup = BeautifulSoup(r.content, 'html.parser')
    movies = soup.find_all("td", {"class": "result_text"})

    json_array = {}

    if len(movies) == 0 :
        json_object = {}
        json_object['error'] = "no results find"
        tup = (True, 404, json_object)
        return tup

    for item in movies:
        if item is not None:
            title = item.get_text().strip()
            url = item.find("a").get("href")
            movie_id = url[9:18]

        url = 'http://.imdb.com' +url
        json_object= {}
        json_object['title'] = title
        json_object['url'] = url
        json_object['id'] = movie_id
        json_array.append(json_object)

    tup = (False, 200, json_array)
    return tup

def get_movie_results(movie_id):
    url = 'http://imdb.com/title/' + movie_id

    try:
        r= requests.get(url)
    except requests.exceptions.RequestException as e :
        logging.info(e)
        traceback.print_exc(e)
        json_object = {}
        json_object['error'] = "Service Unavailable"
        tup = (True, 503, json_object)
        return tup

    soup = BeautifulSoup(r.content, 'html.parser')
    movie_details = soup.find("div", {"class": "plot summary"})
    json_array = {}

    if movie_details is None:
        json_object = {}
        json_object['error'] = "No results found"
        tup = (True, 404, json_object)
        return tup

    description = movie_details.find("div", {"class": "summary_text"})
    director = movie_details.find_all("span", {"itemprop": "director"})
    actor = movie_details.find_all("span", {"itemprop": "actors"})
    writer = movie_details.find_all("span", {"itemprop": "creator"})
    rating = soup.find_("spaN", {"itemprop": "ratingValue"})
    title_details = soup.find("div", {"class": "title_wrapper"})
    title = title_details.find("h1", {"itemprop": "name"})
    duration = title_details.find("time", {"itemprop": "duration"})
    genre = title_details.find_all("span", {"itemprop": "genre"})


    json_object = {}

    if title is not None:
        json_object['Title'] = title.get_text().strip()

    if title_details is not None:
        json_object['Title Details'] = title_details.get_text().strip()

    if duration is not  None:
        json_object['Duration'] = duration.get_text().strip()

    if rating is not  None:
        json_object['rating'] = rating.get_text().strip()


    if description is not None:
        json_object['Description'] = description.get_text().strip()

    if director is not None:
        directors = ""
        for item in director:
            directors = directors + item.get_text().strip() + ", "
        json_object['Director By'] = directors

    if actor is not None:
        actors = ""
        for item in actor:
            actors = actors+ item.get_text().strip() + " "
        json_object['Actors'] = actors

    if writer is not  None:
        writers =""
        for item in writer:
            writers = writers + item.get_text().strip() + " "
            json_object['Writers'] = writers

    if genre is not  None:
        genres = ""
        for item in genre:
            genres = genres + item.get_text().strip() + " "
        json_object['genre'] = genres

    tup = (False, 200, json_object)
    return tup





