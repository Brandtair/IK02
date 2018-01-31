import csv
import urllib.request
import requests
from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def api_query(terms, length = 1000):

    # set the parameters for the query
    payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : terms,
            'to' : length
        }

    # make connection with the API and return the query results
    return requests.get('http://api.edamam.com/search', params=payload).json()

def searchfunction(results):

    # get the images from the recipes
    imglink = []
    for hit in results['hits']:
        imglink.append(hit['recipe']['image'])

    # get the recipe names
    names = []
    for hit in results['hits']:
        names.append(hit['recipe']['label'])

    # get the links where the recipes come from
    urls = []
    for hit in results['hits']:
        urls.append(hit['recipe']['url'])

    # make a dict per recipe and make a list of dicts
    reclist = []
    for i in range(len(imglink)):
        temp = {}
        temp['name'] = names[i]
        temp['img'] = imglink[i]
        temp['url'] = urls[i]
        reclist.append(temp)

    return reclist