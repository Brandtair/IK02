Milan Doodeman, Daan Brandt, Roos Dessing
_______________________________________

# Controller


### Used plugins
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

### Login
request.method == "POST"
Functie ontvangt ingevuld formulier uit view in model(application.py).
model voert programma uit om in te loggen of geeft een foutcode.
controller roep homepage of loginpagina met error op van model naar view.

### Register
request.method == "POST"
Uit view komt er een aanvraag voor een account. De controller redirect html template voor het aanmaken van een account.
Hier kom je bij de view van een registerpagina. Vanuit de registreerpagina kan je je een gebruikersnaam invoeren die wordt doorgestuurd naar de juiste afdeling waar de gebruikersnaam wordt opgeslagen in het python programma. Bestaat de gebruiksnaam al dan stuurt de controller een error van model naar view. Nadat de gebruikersnaam is opgeslagen kan er een wachtwoord worden ingevoerd. Deze wordt doorgestuurd naar een pagina waar het in encrypt wordt opgeslagen. Het wachtwoord moet vervolgens worden herhaald, match het met de eerste invoer dan kan de pagina worden geregistreerd, anders stuurt de pagina een view met een error dat het wachtwoord niet matcht. Als het account geregistreerd kan worden stuurt de controller het account naar de pagina waar het account wordt opgeslagen en roept de controller de index(homepage) op.  

### Index

Vanaf het model van de index pagina stuurt de controller een view van de homepagina.
Op de homepagina is er een mogelijkheid om naar je eigenpagina te gaan, een mogelijkheid om voorkeuren te zien van recepeten gebaseerd op de voorkeuren vastgesteld in jou persoonlijkepagina, een mogelijkehid om recepten op te zoeken, een mogelijkheid om recepten op te slaan en een mogelijkheid om recepten naar vrienden te sturen.

- Er gaat een link naar de persoonlijkepagina
- De voorkeuren komenvoort uit een ingaande link vanaf een pagina waar de opgeslagen voorkeuren van de persoonlijkepagina staan opgeslagen. De recepten hebben een link die de gebruiker stuurt naar een view van de desbetreffende pagina van het recept. Vanaf deze html wordt de gebruiker weer redirected naar de indexpagina wanneer de gebruiker het recept wegklikt.
- De recepten op de homepagina dragen de mogelijkheid om te worden opgeslagen. Het recept heeft een link die verstuurd wordt naar een pagina van opgeslagen recepten. Ook kan er wanneer er op de recepten wordt geklikt een
- Op de receptenpagina moet een refreshbutton komen om elke keer nieuwe recepten toe te voegen. De controller zorgt ervoor dat er link gaat naar de database van recepten en dan random aan de hand van een ingaande link recepten opnieuw weer geeft.

### Personalpage
request.method == "GET"
Op de persoonlijke pagina moeten er gegevens kunnen worden ingevuld die worden doorgestuurd naar een pagina waar deze zijn opgeslagen zodat ze kunnen worden doorgeschakkeld via de controller. Op de persoonlijkepagina kunnen er voorkeuren worden opgeslagen voor recepten. Dit zijn stuk voor stuk links die via de contoller later worden doorgestuurd naar de homepage. Om random te verschijnen.

### Search 
request.method == "GET"
Op homepage moet er een searchbalk zijn met een link via de contoller naar de database van recepten. Deze dient als filter te werken. Elke keer als er een filter wordt toegepast hoort er van de selectie views worden weergegeven van de recepten. Deze worden opgeroept door de in link van het gegeven filter. 


### Favorites
request.method == "GET"
Via een inkomende link kom je bij de favorieten pagina. Hier verschijnt een view van de inkomende links van vastgelegde favorieten. Die komen uit van een apart opgeslagen datadeel in python. Op deze pagina moet je per favoriet in favorieten het openen zodat er een aparte view voorkomt. Ook moet er een knop zijn om een favoriet te verwijderen uit favorieten. Deze favoriet moet dan verwijderd worden van de favorietenpagina en verwijderd worden uit de opgeslagen data. Hierbij moet de view van het specifieke recept niet meer worden weergegeven in de pagina, maar worden terug gestuurd naar de index.

### Share
request.method == "GET"
 Via een inkomende link dat er op een recept is geklikt. Komt er een view met het gekozen recept. 
 Het desbetreffende recept moet een uitgaande link hebben om naar een nieuwe view te komen met een mogelijkheid de link van het recept door te sturen. Dit moet een uitgaande link zijn die doorstuurt naar het model van de deelfunctie.
 


_______________________________________

# MODELS HELPERS


### IK02
ComputerScience group IK02


### Register

def register():

request.method == "POST"
  
  function username
    check if username is not in already in use.
    display "username not availble" if username in use.
  Next-button saves username in variable.
  
  function password
    hash password
  Next-button saves password in variable.
  
  function check password
    If password is equal to variable
      save password in dict.
    send password to database

### Login

def login():

request.method == "POST"

  function username
    check if valid.
    request valid usernam if not valid
  function password
    check if valid.
    display "wrong password" if password not valid.
  Login button sends form.

### Homepage

def recepes():
  render request 4 recepes from database.
  filter tot naam, bereidingsrijd en afbeelding.

### Account

def wijzig_gegevens():

request method == "POST"


  function Username():
    check if valid
    if not valid apologise "please fill in Username"
    
  function Password():
    check if valid
    if not valid apologise "Please fill in Password"
    
  function NewPassword():
    check if valid
    if not valid & equal apologise "please fill in new password"
    
  Button "save"
  
def wijzig_filter():

  clear.session()
  
  function Dieet():
    add 

### Change Personalpage

def settings():
  
  def wijzig_settings():

  clear.session()
  
  function Dieet():
    add 

  function Ingerienten():
    add 
  
  function Producten():
    add 

  function Keuken():
    add 
  
  function ect.():
    add 
### Search for Recipies

def search():
  get_string
  if string in data
    return data

def refresh():
  
  click button:
    if data in database not in homepage:
      pick random 20 from out of database
      place on homepage
    if data in database in homepage:
      return refresh 
      

### Page for Favorite Recipies
datafavorites = []

for click in homepage favorite:
  datafavorites += recept

def favorites():
    for data in datafavorites:
      place in favoritepage
     

### Page to share Recipies

string = 0

def share(): 
  if click on recept:
    copy link recept = link
    string += link

get email adress
get link
share link 
send link
show succesfully send if so
_______________________________________

# Plugins en Frameworks

We nemen finance als voorbeeld. Hierin wordt Flash gebruikt en Bootstrap. 
Deze willen wij ook toevoegen maar slechts als basis. 

_______________________________________

# Views 

In slack hebben we een presentatie geupload. Hierin staat hoe alle view eruit moeten komen te zien.

https://webik.slack.com/files/U8NSF500H/F8R0PJZ16/visueel_projectplan_ik02.pptx


_______________________________________

# Projectvoostel (aangepast):

In de webapplicatie kunnen gebruikers hun persoonlijke wensen en voorkeuren aangeven , op een eigen pagina, voor het kiezen van een recept. Aan de hand hiervan stelt de app recepten voor die van toepassing zijn op de persoonlijke wensen van de gebruiker. Ook biedt de app een mogelijkheid om recepten te sorteren op voorkeur van ingrediënten, smaak ect. 

Recepten kunnen worden opgeslagen als favoriet en worden gedeeld met andere gebruikers.

<img src="http://preview.ibb.co/jTYBXR/IMG_4477.jpg" />

<img src="http://preview.ibb.co/bH2S6m/IMG_4478.jpg" />

Loginpage:

- Een persoon kan inloggen als diegene al een account heeft op de app of een nieuw account aanmaken als diegene nog geen account heeft.

Account maken:

- Hier moet de persoon zijn naam, wachtwoord, voorkeuren voor recepten (op basis van ingrediënten) invullen. 

Homepage:

- Hier ziet de gebruiken recepten die worden voorgesteld op basis van de voorkeuren, kan de gebruiken zoeken op recepten, de ingevoerde gegevens wijzigen (denk aan wijzigen van voorkeuren).

Favoritespage:

- Hier kan de gebruiker opgeslagen recepten zien, deze recepten bekijken en deze verwijderen.

Op elk gewenst moment kan de gebruiker uitloggen en teruggaan naar de loginpage.

Om een MVP te maken zijn de volgende functies essentieel

- Het zoeken van de recepten;

- Het opslaan van favorieten;

- Het delen van recepten met vrienden;

- Dus het hebben van een eigen account.

*Bij het aanmaken van een account moet het mogelijk zijn om wijzigingen aan te brengen. Dit gaat doormiddel van 1 knop die wijzigingen toestaat en 1 knop die wijzigingen opslaat. 

Afhankelijkheden:

Databronnen:

- De API met recepten die wij gaan gebruiken voor onze applicatie: https://developer.edamam.com/

Externe componenten:

- CS50 voor het programmeren, van de rest van de externe componenten zijn wij nog niet op de hoogte.

Concurrerende bestaande websites:

- AH allerhande recepten: een site waar recepten geordend staan onder bepaalde categorieën en waar de gebruiker kan zoeken op dingen waar hij trek in heeft.

- Smulweb: hier kan de gebruiker zoeken op recepten en staan er veel voorgestelde recepten onder de zoekbalk.

Moeilijkste delen:

- De moeilijkste delen van de app worden het wijzigen van de gegevens, het delen van recepten met vrienden en de inlogpagina. Ook het bijhouden van persoonsgegevens wordt lastig.
