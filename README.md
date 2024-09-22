# ruokatietopankki

Sivuston tarkoituksena on näyttää käyttäjälle tietoa eri ruokien ravintoarvoista sekä mahdollistaa omien reseptien luonti ja annosten ravintosisällön tarkastelu.

Ominaisuuksia:
- [x] Käyttäjä pystyy hakemaan selaamaan ruokia etusivulla
- [x] Käyttäjä näkee kunkin ruuan ravintosisällön tiivistettynä (energia, rasva, hiilihydraatti, proteiini) etusivun listauksessa
- [x] Käyttäjä voi painaa ruokaa listauksesta, jolloin siitä näytetään enemmän tietoa (tyydyttyneet rasvat, sokeri, kuidut)
- [x] Käyttäjä pystyy hakemaan tiettyä ruokaa
- [ ] (Mahdollinen lisäominaisuus: haun fuzzy matching)
- [ ] Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- [ ] Käyttäjä pystyy lisäämään (ja poistamaan) ruokia suosikiksi
- [ ] Käyttäjä pystyy tarkasteleman omia suosikkejaan
- [ ] Käyttäjä pystyy luomaan (ja poistamaan reseptin) ja liittämään (ja poistamaan) reseptiin ruokia haluttu määrä


Ruoka-aineiden lähteenä käytetään ainakin fineli.fi avointa dataa


## Tilanne 22.9.2024

Sovelluksessa on toimiva runko. Käyttäjä näkee heti etusivulla dynaamisesti päivittyvän taulukon ruoista. Taulukko on tehty Grid.js:n avulla. Mallia taulukon tekemiseen otettiin Miguel Grinbergin blogista (https://blog.miguelgrinberg.com/post/beautiful-flask-tables-part-2). Taulukko näyttää siis food_stats taulun rivit hakien ne aina sivun kerrallaan. Taulukkoa pystyy järjestämään nimen mukaan. Siitä pystyy myös hakemaan eri ruoka-aineta. Taulukon ensimmäinen sarake näyttää ruuan id:n (foodid) ja se toimii samalla linkkinä kyseisen ruuan sivulle (@app.route("/foodpage/<int:id>")).

Seuraavana tehtävälistalla on ensin yksittäisen ruokasivun kehittäminen ja sen jälkeen kirjautumisen luominen. Kirjautumisen luomisen yhteydessä tietokantaan luodaan käyttäjään liittyvät taulut, kuten users, user_favourites, user_recepies yms. Lisäksi täytyy tehdä uudet sivut käyttäjän suosikkien sekä reseptien näyttämiselle.


## Testaus omalla koneella:

Miten testata sivun toiminta omalla koneella:
+ HUOM! oletuksena on että käytössäsi on linux ja siihen on asennettu PostgreSQL
1. kloonaa tämä repositorio omalle koneellesi (linux) (katso materiaalin Osa 3 - versionhallinta)
2. luo uusi virtuaaliympäristö
3. asenna vaaditut riippuvuudet (virtuaaliympäristössä: pip install -r requirements.txt)
4. luo tietokantaan 1 taulu (food_stats), jonka ddl löytyy schema.sql-tiedostosta
5. aja ruokadata tauluun joko ajamalla ./data/food_stats_sql.sql-tiedoston INSERT INTO lauseet tai sitten kopiomalla ./data/food_stats.csv tiedosto bulkkina postgreen komentorivin kautta
    esim. näin (huom, vaihda tiedoston polku oikeaksi):
    \copy food_stats (foodid,foodname,energia_laskennallinen,rasva,hiilihydraatti_imeytyvä,hiilihydraatti_erotuksena,proteiini,alkoholi,tuhka,vesi) FROM '/home/pubuntu/harkkatyo/food_stats.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF-8';

6. säädä app.py:n tietokantayhteys sinun tietokannan mukaiseksi
    (eli rivin 8 koodi: app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres")
7. aktivoi venv, navigoi src/ kansion sisälle ja käynnistä flask (flask run)
8. mene selaimella osoitteeseen http://127.0.0.1:5000, jolloin pitäisi avautua aloitussivu taulukkoineen
