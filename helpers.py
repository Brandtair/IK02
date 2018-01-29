import csv
import urllib.request
import requests
from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    print(message)
    return render_template("apology.html", top=code, bottom=escape(message)), code


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
    print("TERMS ===================== ",terms)
    payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : terms,
            'to' : length
        }

    return requests.get('http://api.edamam.com/search', params=payload).json()

def searchfunction(results):
    imglink = []
    for hit in results['hits']:
        imglink.append(hit['recipe']['image'])

    names = []
    for hit in results['hits']:
        names.append(hit['recipe']['label'])

    urls = []
    for hit in results['hits']:
        urls.append(hit['recipe']['url'])

    reclist = []
    for i in range(len(imglink)):
        temp = {}
        temp['name'] = names[i]
        temp['img'] = imglink[i]
        temp['url'] = urls[i]
        reclist.append(temp)

    return reclist