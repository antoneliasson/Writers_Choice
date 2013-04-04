Planering
=========
Klara stories: 1-11

Story 1
=======
Projektet använder MVC-ramverket Pyramid och utgår från mallen alchemy. Detta innebär att SQL Alchemy används som lagringsmekanism och URL Dispatch används för att koppla URL:er till vyer.

Story 2
=======
Programmet hanterar artiklar. Varje artikel består av ett id-nummer, publikationsdatum, rubrik och brödtext. Brödtexten skrivs i Markdown. Användare kan visa en artikel genom att besöka webbadressen `http://<url>/<id>`.

Task 2.1
--------
Ny modell `Article` bestående av fälten `id` (heltal, primär nyckel), `title` (sträng), `body` (mediumtext), `published` (tidsstämpel).

Task 2.2
--------
Ny vy `view_article` som tar en artikels id-nummer som argument. Vyn returnerar en dictionary med artikelns rubrik, HTML-kompilerad brödtext och datum publicerad (formaterat som ÅÅÅÅ-MM-DD) som renderas med den nya mallen `view`.

Task 2.3
--------
Ny mall `view` som utgår från standardmallen `mytemplate`. Den ska visa en artikels brödtext under dess publikationstid under dess rubrik.

Task 2.4
--------
Rutten /{id} kopplas till vyn `view_article`.

Story 3
=======
Användaren kan visa alla artiklar efter varandra sorterade efter publiceringsdatum (nyast överst) genom att besöka startsidan (`http://<url>/`). Startsidan kommer att ha flera h1-rubriker.

Task 3.1
--------
Ny vy `view_all`. Den funkar på samma sätt som `view_article` men returnerar en lista av dictionaries bestående av title, published och body för varje artikel.

Task 3.1
--------
Kopiera mallen `view` till `view_all`. Sätt hela artikeln (h1, div id=published, div id=body) i den nya mallen inom en div som repeteras för varje artikel i listan. Ändra id till class.

Task 3.3
--------
Rutten / kopplas till vyn `view_all`.

Story 4
=======
Användaren kan lägga till nya artiklar genom att besöka webbadressen `http://<url>/add`. På denna sida finns textrutor för inmatning av den nya artikelns rubrik och brödtext.

Task 4.1
--------
Ny vy `add_article`. Denna POSTar en ny artikel till sig själv. Om vyn anropas som ett resultat av en POST sparas den nya artikeln i databasen. Därefter skickas användaren till `view_article` för den aktuella artikeln.

Task 4.2
--------
Ny mall `add_article`. Denna visar en HTML-form med två textrutor. Submitknappen skickar till vyn `add_article`.

Task 4.3
--------
Rutten /add kopplas till vyn `add_article`.

Task 4.4
--------
På startsidan visas en länk till vyn `add_article`.

Story 5
=======
Användaren kan redigera befintliga sidor genom att besöka webbadressen `http://<url>/edit/<id>`. På denna sida finns textrutor för rubrik och brödtext precis som i story 4. Här är de ifyllda med de befintliga värdena.

Task 5.1
--------
Ny vy `edit_article`. Denna fungerar precis som `add_article` men plockar först ut den befintliga artikeln ur databasen (baserat på dess id) och returnerar den tillsammans med en länk till sig själv för att spara artikeln. POST till sig själv hanteras som i Story 4.

Task 5.2
--------
Ny mall `edit_article`. Denna fungerar som mallen `add_article` men textrutorna fylls i vid laddning.

Task 5.3
--------
Rutten /edit/{id} kopplas till vyn `edit_article`.

Task 5.4
--------
Vyn `view_article` redigeras för att även returnera en länk till `edit_article`-vyn för aktuell artikel.

Task 5.5
--------
Mallen `view_article` redigeras för att visa en länk till `edit_article`-vyn för aktuell artikel.

Story 6
=======
Artiklarna ska visas sorterade efter publiceringsdatum, nyast först, på startsidan. Detta missades i implementationen av Story 2.

Story 7
=======
På artikelvisningssidorna visas titeln som en h1-rubrik. Rubriker som förekommer i brödtexten börjar på h2 (för #) och fortsätter uppåt (mot högre ordningsnummer).

Story 8
=======
På startsidan visas artiklarnas titlar som h2-rubriker. Rubriker som förekommer i brödtexten börjar på h3 (för #) och fortsätter uppåt (mot högre ordningsnummer).

Story 9
=======
På startsidan ska artiklarnas rubriker länka till artikelvisningssiddan för aktuell artikel.

Story 10
========
Överst på startsidan ska webbplatsens titel visas. För närvarande är den hårdkodad till Writer's Choice. Titeln ska länka till startsidan.

Story 11
========
Tabeller skrivna enligt Pythons officiella (nåja) Markdownimplementation ska omvandlas till HTML-tabeller.

Story 12
========
Artiklar har endast heltal som IDn. Rutten till vyn `view_article` ska reflektera detta.

Story 13
========
Ångra story 12. Länkarna till artikelvisningssidorna ska vara på formatet `http://<url>/<id>/<slug>` där "slugen" genereras från artikelns rubrik. ID-fältet tar allt fram till /.  Slugen tar resten av URLen. Den är inte nödvändigtvis unik och används inte av `view_article` vid uppslagning av rätt artikel.

Story 14
========
Även URLen som genereras av `add_article` och `edit_article` ska ha formatet som beskrivs i Story 13.

Story 15
========
Vyn `view_article` ska först kolla om slugen är den förväntade, annars omdirigerar den till sig själv via rutten `view_article_slug` med rätt slug.

Story 16
========
Byt teckensnitt på alla sidor till några enkla och snygga sans-serif. Brödtexten ska vara justerad (justified).

Story 17
========
Rubrikfältet i edit- och add-lägena ska vara runt 80 tecken bred. Brödtextboxen ska vara runt 80x24 tecken stor. Det här är standardstorlekarna. Jag kommer nog fiffla en del med storlek och placering i CSS senare.

Story 18
========
(borttagen)

Story 19
========
Add- och edit-lägena ska ha ytterligare en submit-knapp som avbryter redigeringen. Den skickar till samma sida men har ett annat namn. Vyerna omdirigerar en till sig själv via GET utan att spara datan som POSTades med formen.

Story 20
========
Försöker man visa en sida som inte finns (som fångas av `view_article`) ska en enkel 404-sida visas.
