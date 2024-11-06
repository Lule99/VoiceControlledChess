# VoiceControlledChess
Predmetni projekat za predmet Soft Computing.
## Opis problema
Rešava se problem igranja šaha gde će komande biti dobijane govorom na srpskom jeziku. Za detekciju govora se koriste dve neuronske mreže, jedna za slova a druga za cifre.
## Podaci
Podaci za neuronsku mrežu koja prepoznaje govor su pravljenji specijalno za ovaj projekat. Sam dataset se može podeliti na dva dela. Dataset gde su podaci brojevi sa klasama 1-8 i drugi-slova sa klasama A-H. Prvi dataset broji 105 originalna audio zapisa po klasi gde je odnos ženskih i muških glasova oko 40:60. Dataset za slova sadrži nešto više snimaka po klasi, odnosno 151 snimak sa sličnim odnosom muških i ženskih glasnova. Oba dataseta su strogo balansirana i svaka klasa sadrži jednak broj elemenata. Proširenje inicijalnog dataseta obezbeđeno je raznim postupcima augmentacije, detaljno opisanim u augmentations.py, a koji su se prevashodno svodili na dodavanje različitog nivoa pozadinskog šuma, promena visine tonova, ubrzavanjem, usporenjem i pojačavanjem po potrebi (određene grupe snimaka bile su veoma slabog intenziteta te je izvršeno pojačavanje za 30db). Nakon postupka augmentacije, klase dva dataseta brojala su 1155 i 1661 element respektivno, odnosno inicijalni dataset uvećan je 11 puta. Nad ovako dobijenim podacima izvršen je postupak normalizacije i skaliranja na 128x128 piksela, obzirom na hardwersko ograničenje mašine na kojoj je vršeno testiranje (4 GB memorije na grafičkoj kartici).
## Agentski Algoritam
Obzirom da šah predstavlja igru nulte sume, kao agentski algoritam odabran je minimaks sa alfa-beta odsecanjem. Potreba za evaluacijom velikog broja pozicija minimaks algoritma nameće se kao osnovno ograničenje u radu agenta, te je u tom smislu implementirana heuristička funkcija manje kompleksnosti koja u obzir uzima broj i vrstu figura na tabli, kao i njihovu poziciju na osnovu tipa figura.
##Modul Za Rad Sa Zvukom
Modul za rad sa zvukom obuhvata funkcionalnosti potrebne za prepoznavanje odnosno klasifikaciju izgovorenih polja (što predstavlja ulazne podatke), kao i funkcionalnosti za snimanje, dalju obradu, manipulaciju, augmentaciju i obuku modela za klasifikaciju.

## Pokretanje
Da bi se pokrenuo projekat potrebno se prvo pozicionirati na root folder projekta i instalirati sve neophodne zavisnosti iz fajla requirements.txt komandom ``` pip install -r requirements.py```
Nakon toga, potrebno je pokrenuti komandu ```python main.py```i odabrati level i algoritam. Na kraju, nakon sto se na konzoli prikaže znak za govor treba jasno reći polje koje selektujemo (E2) sa malom pauzom između glasova. Zatim nakon što mreža prepozna selekciju potrebno je uneti na isti način odredište.

## Dokumentacija
Prateća prezentacija kao i demo rada aplikacije se nalazi u folderu "Dokumentacija".
