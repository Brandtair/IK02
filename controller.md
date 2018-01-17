# Controller
## Used plugins
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

## Login
request.method == "POST"
Functie ontvangt ingevuld formulier uit view in model(application.py).
model voert programma uit om in te loggen of geeft een foutcode.
controller roep homepage of loginpagina met error op van model naar view.

## register
request.method == "POST"
Uit view komt er een aanvraag voor een account. De controller redirect html template voor het aanmaken van een account.
Hier kom je bij de view van een registerpagina. Vanuit de registreerpagina kan je je een gebruikersnaam invoeren die wordt doorgestuurd naar de juiste afdeling waar de gebruikersnaam wordt opgeslagen in het python programma. Bestaat de gebruiksnaam al dan stuurt de controller een error van model naar view. Nadat de gebruikersnaam is opgeslagen kan er een wachtwoord worden ingevoerd. Deze wordt doorgestuurd naar een pagina waar het in encrypt wordt opgeslagen. Het wachtwoord moet vervolgens worden herhaald, match het met de eerste invoer dan kan de pagina worden geregistreerd, anders stuurt de pagina een view met een error dat het wachtwoord niet matcht. Als het account geregistreerd kan worden stuurt de controller het account naar de pagina waar het account wordt opgeslagen en roept de controller de index(homepage) op.  

## index


## personalpage


## search

## favorites

## share


