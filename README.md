# ruokatietopankki

Sivuston tarkoituksena on näyttää käyttäjälle tietoa eri ruokien ravintoarvoista sekä mahdollistaa omien reseptien luonti ja annosten ravintosisällön tarkastelu.

Ominaisuuksia:
- [x] Käyttäjä pystyy hakemaan selaamaan ruokia etusivulla
- [x] Käyttäjä näkee kunkin ruuan ravintosisällön tiivistettynä (energia, rasva, hiilihydraatti, proteiini) etusivun listauksessa
- [x] Käyttäjä voi painaa ruokaa listauksesta, jolloin siitä näytetään enemmän tietoa (tyydyttyneet rasvat, sokeri, kuidut)
- [x] Käyttäjä pystyy hakemaan tiettyä ruokaa
- [ ] (Mahdollinen lisäominaisuus: haun fuzzy matching)
- [x] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- [x] Käyttäjä pystyy lisäämään (ja poistamaan) ruokia suosikiksi
- [x] Käyttäjä pystyy tarkasteleman omia suosikkejaan
- [x] Käyttäjä pystyy luomaan (ja poistamaan reseptin) ja liittämään (ja poistamaan) reseptiin ruokia haluttu määrä


Ruoka-aineiden lähteenä käytetään ainakin fineli.fi avointa dataa


## Tilanne 22.9.2024

Sovelluksessa on toimiva runko. Käyttäjä näkee heti etusivulla dynaamisesti päivittyvän taulukon ruoista. Taulukko on tehty Grid.js:n avulla. Mallia taulukon tekemiseen otettiin Miguel Grinbergin blogista (https://blog.miguelgrinberg.com/post/beautiful-flask-tables-part-2). Taulukko näyttää siis food_stats taulun rivit hakien ne aina sivun kerrallaan. Taulukkoa pystyy järjestämään nimen mukaan. Siitä pystyy myös hakemaan eri ruoka-aineta. Taulukon ensimmäinen sarake näyttää ruuan id:n (foodid) ja se toimii samalla linkkinä kyseisen ruuan sivulle (@app.route("/foodpage/<int:id>")).

Seuraavana tehtävälistalla on ensin yksittäisen ruokasivun kehittäminen ja sen jälkeen kirjautumisen luominen. Kirjautumisen luomisen yhteydessä tietokantaan luodaan käyttäjään liittyvät taulut, kuten users, user_favourites, user_recepies yms. Lisäksi täytyy tehdä uudet sivut käyttäjän suosikkien sekä reseptien näyttämiselle.


## Tilanne 6.10.2024

Käyttäjä näkee kirjautumatta kaikki ruuat listattuna. Ruoka-taulukossa on linkki kunkin ruuan tarkemmalle tuotesivulle. Ruokien listauksessa on käytetty dynaamista Grid.js-taulukkoa, koska ruokia on tietokannassa 4232 eli staattinen HTML taulukko ei ole järkevä ratkaisu. Muut taulukot (esim. suosikkiruuat) on tehty HTML-taulukoiden ja suorien tietokantakyselyiden avulla.

Käyttäjä pystyy kirjautumaan sovellukseen. Kirjautuneena käyttäjä pystyy lisäämään ruokia suosikiksi kunkin ruuan tuotesivuilta. Kirjautuneen äyttäjän suosikit näytetään etusivulla näkee suosikkiruokansa. Käyttäjä pystyy luomaan uusia reseptejä http://127.0.0.1:5000/create_recipe sivulla. Reseptillä on nimi, kuvaus ja n kappaletta ruokia ja niiden painot grammoina.

Seuraavana tehtävälistalla on muun muassa ulkoasun siistiminen, koodin refactorointi (esim. app.py:n funktioiden siirto asianmukaisiin moduuleihin), koodin kommentointi ja tietoturva-asioiden tarkastaminen.


## Lopullinen palautus 20.10.2024

#### Sovelluksen toiminta käyttäjän näkökulmasta:
Sovelluksen etusivulla näkyy taulukko kaikista ruoka-aineista. Käyttäjä pystyy selaamaan taulukkoa kirjautumatta. Taulukon ensimmäisessä sarakkeessa on linkki tarkemmalle tuotesivulle.

Etusivulta käyttäjä pystyy joko kirjautumaan sisään tai luomaan tunnuksen. Kirjautunut käyttäjä näkee etusivulla omat suosikiksi merkkaamansa ruuat sekä käyttäjän luomat reseptit. 

#### Sovelluksen toiminta palvelimella:
Sovellus tarkistaa käyttäjän syötteet sekä käyttöliittymässä että palvelimella. Käyttäjälle annetaan virheilmoitus virheellisestä syötteestä jo käyttöliittymässä, mutta myös palvelimelta, jos pyyntö pääsee sinne asti. 

Suurin osa taulukoista on tehty HTML taulukkoina suorien SQL-kyselyiden avulla. Kaikki ruoka-aineet näytetään Grid.js taulukon avulla rivimäärän ollessa sen verran iso.

Tietoturvaa on mietitty käyttäjän syötteiden tuplatarkistuksella, parametrisoituina kyselyinä sekä CSRF suojauksella.

Ruoka-aineiden lähteenä käytetään avointa dataa osoitteesta fineli.fi. Data tulee ladata alla olevien ohjeiden mukaan tietokantaan ennen sovelluksen testausta.


## Testaus omalla koneella:

Miten testata sivun toiminta omalla koneella:
+ HUOM! oletuksena on että käytössäsi on linux ja siihen on asennettu PostgreSQL
1. kloonaa tämä repositorio omalle koneellesi (linux) (katso materiaalin Osa 3 - versionhallinta)
2. luo uusi virtuaaliympäristö ja asenna vaaditut riippuvuudet:
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
3. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
```
DATABASE_URL="<tähän-sinun-tietokannan-paikallinen-osoite>"
SECRET_KEY="<tähän-sinun-generoima-salainen-avain>"
```
+ oman salaisen avaimen voi luoda vaikka Pythonilla linuxin terminaalissa esim. näin:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```
4. luo taulut tietokantaan joko ajamalla ```$ psql < schema.sql``` tai ajamalla ne käsin tietokannassa
+ HUOM! lisää tauluihin haluamasi schema mikäli haluat luoda ne johonkin muuhun kuin oletus (=public) schemaan
5. aja ruokadata tauluun. Hidas tapa on ajaa ./data/food_stats_sql.sql-tiedoston INSERT INTO lauseet esim. näin:
```psql < src/data/food_stats_sql.sql```
Nopeampi tapa on kopioida ./data/food_stats.csv tiedosto bulkkina tietokantaan postgren komentorivin kautta esim. näin (huom, vaihda tiedoston polku oikeaksi):
```
\copy food_stats (foodid,foodname,energia_laskennallinen,rasva,hiilihydraatti_imeytyva,hiilihydraatti_erotuksena,proteiini,alkoholi,tuhka,vesi) FROM '/home/pubuntu/harkkatyo/food_stats.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF-8';
```
7. navigoi src/ kansion sisälle ja käynnistä flask (flask run)
8. mene selaimella osoitteeseen http://127.0.0.1:5000, jolloin pitäisi avautua aloitussivu taulukkoineen
