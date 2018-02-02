# Makes Right Diner
### Daan Brandt, 11865970, Roos Dessing, 11796847, Milan Doodeman, 11784210

#### Screenshot van login-pagina
<img src="https://preview.ibb.co/dfJ6M6/a863e882_cbe0_4161_bb59_34f9777185ca.jpg" />

#### Video van website
https://www.youtube.com/watch?v=S4Mt5uZFRLE (not yet finished)

#### Functionaliteit
In de webapplicatie kunnen gebruikers hun persoonlijke voorkeuren, maar ook eventueel dieet en allergieën aangeven. Op de persoonlijke pagina van de gebruiker ziet de gebruiker steeds 3 willekeurige gerechten die voldoen aan minimaal 1 van de opgegeven voorkeuren, maar ook aan de opgegeven dieetwensen en allergieën. Er is ook de mogelijkheid om naar recepten te zoeken op basis van naam of ingrediënt. Dit kan zowel ingelogd als niet ingelogd. Als er wel is ingelogd, houdt de applicatie rekening met de opgegeven dieetwensen en allergieën. Als er niet is ingelogd laat de applicatie alle gevonden recepten zien. Recepten kunnen worden opgeslagen als favoriet en worden bekeken op een speciale pagina. Alle gevonden recepten kunnen worden gedeeld met iedereen met een mailaccount doormiddel van een ingebouwde mailfunctie. 
 
#### Korte taakverdeling
Daan heeft zich vooral gefocust op de opmaak van de html bestanden en de overall opmaak van de site door middel van css. Soms wat python maar vooral het leren van css en het maken van de view. 
Roos heeft zich niet op 1 ding gefocust. Zij heeft van alles een beetje gedaan: het maken van html pagina's en het programmeren van functies in python.
Milan heeft zich vooral met de functies van python beziggehouden. Af en toe een html pagina maken, maar vooral de lastigheden in de application en wat troubleshooten hier en daar. 

#### Wegwijzer repository
- In application.py staat hoe de site werkt, wat er met alle verstuurde data wordt gedaan en hoe overal naar verwezen wordt. 
- In helpers.py staan een paar functies die zo vaak werden herhaald in application dat een eigen functie maken praktischer was. De functies zijn een check of er is ingelogd, een functie voor de verbinding met de api, en een functie die gegevens verzamelt van de recepten na het zoeken van een recept.
- Project.db is de database die is gebruikt om de gebruikers met hun gegevens en de opgegeven favorieten op te slaan. Er zijn twee tables, users voor de gebruikers en favorites voor de favorieten.
- In de map templates staan alle html files die gebruikt zijn voor de view van de pagina. 
