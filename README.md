# VoiceControlledChess
Predmetni projekat za predmet Soft Computing.
## Opis problema
Rešava se problem igranja šaha gde će komande biti dobijane govorom, i to na srpskom jeziku. Za detekciju govora se koriste dve neuronske mreže, jedna za slova a druga za cifre.
## Podaci
Podaci za neuronsku mrežu koja prepoznaje govor su pravljenji specijalno za ovaj projekat. Vrši se prvo proširenje skupa augmentacijom a onda se pretvara zvuk u mel spektogram koji se prosledjuje mreži.
Takođe, za algoritam šaha se koristi mreža koja procenjuje da li je potez pobednički gubitnički ili dovodi do nerešenog ishoda na osnovu podataka iz 20000 partija. [Set podataka](https://database.lichess.org/).

## Pokretanje
Da bi se pokrenuo projekat potrebno se prvo pozicionirati na root folder projekta i instalirati sve neophodne zavisnosti iz fajla requirements.txt komandom ``` pip install -r requirements.py```
Nakon toga, potrebno je pokrenuti komandu ```python main.py```i odabrati level i algoritam. Na kraju, nakon sto se na konzoli prikaže znak za govor treba jasno reći polje koje selektujemo (E2) sa malom pauzom između glasova. Zatim nakon što mreža prepozna selekciju potrebno je uneti na isti način odredište.

## Clanovi tima
- Luka Kureljušić sw-23-2018
- Đorđe Njegić sw-12-2018
- Njegoš Blagoejvic sw-18-2018
