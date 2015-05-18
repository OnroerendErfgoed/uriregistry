===========
Opmerkingen
===========

Enkele opmerkingen

CAP theorem
-----------

Het deleten van een object in een authentieke bron is een operatie die niet altijd uitgevoerd kan worden.
Dit omdat we er voor kiezen om consistentie te behouden. Volgens het 'CAP theorem' verliezen we hierdoor
beschikbaarheid of tolerantie van het systeem.

Beschikbaarheid verliezen is volgens mij onaanvaardbaar. Het systeem zal soms blijven hangen of de client krijgt geen antwoord.
Bij het verliezen van tolerantie, zal een delete niet mogelijk zijn als een deel van de systemen binnen het domein niet beschikbaar zijn.

De delete operatie is dus consistent en beschikbaar, maar niet tolerant. Er zijn ook andere opties, zie hieronder.

-----

CAP theorem definieert drie eigenschappen van een gedistribueerd systeem:

* Consistency (Consistentie): Data opvragen van het systeem geeft altijd de meest up-to-date data.
* Availability (Beschikbaarheid): Elke request slaagt of faalt(er wordt niet gewacht tot alle systemen gerecovered zijn)
* Partition tolerance (Tolerantie): Het systeem blijft werken, zelfs als bepaalde services niet beschikbaar zijn

Het CAP theorem stelt dat je slecht twee van de drie eigenschappen kan hebben:

* Als een systeem consistent en tolerant is dan verliest het beschikbaarheid - je zal mogelijk moeten wachten op een reponse tot dat het systeem hersteld is.
* Als een systeem consistent en beschikbaar is dan zal je mogelijk downtime hebben (dit hoeft niet het hele systeem te zijn, maar de operatie die consistent en beschikbaar is)
* Als een systeem beschikbaar en tolerant is zal je mogelijk inconsistente data hebben


ACID
----

Het zal zeer moeilijk zijn om 100% data consitentie te garanderen in dit syteem. Vooral omdat er niet voldaan kan worden aan het ACID principe.
Voor de isolatie van operaties is een probleem hier. Een gedistribueerd systeem als dit, zal dit niet kunnen garanderen.

Het kan bijvoorbeeld zijn dat een authentieke bron al geantwoord heeft dat het geen referenties meer heeft voor een bepaalde uri.
Maar dat een gebruiker op dat moment toch een nieuwe referentie aanmaakt. De uri links zijn soft links en worden dus niet gevalideerd na het aanmaken.

----

ACID (Atomicity, Consistency, Isolation, Durability)


BASE
----

Dit model is komt beter overeen met onze data. Er wordt zoveel mogelijk gefocust op beschibaarheid van data. En qua consistentie focust men vooral op
eventual consistency (uiteindelijk zal alles wel consistent zijn). Er wordt hier mmestal wel gebuik gemaakt van een vorm van conflict resolution om problemen op te lossen.

----

BASE (Basically Available, Soft state, Eventual consistency)


Conclusie
---------

Er zijn twee mogelijkheden om de links tussen data zo veel mogelijk consistent te houden. Mogelijk moeten beide geimplementeerd worden:

1. Als een authentieke bron een resource wil verwijderen, checkt het via een centrale repository of deze resource nog gelinkt wordt via de uri van de resource.
Indien niet, mag de resource verwijdert worden.
De keuze die hier nog moet gemaakt worden is, wat te doen indien niet alle authentieke bronnen beschikbaar zijn. Er kan voor geopteerd worden om de delete dan niet uit te voeren,
wat de meest consistente data zal opleveren. Ofwel wordt de delete wel uitgevoerd en is er mogelijk inconsistente data.

2. Een authentieke bron voert op regelmatige tijdstippen controles uit op zijn gelinkte data. Er wordt dan gecontroleerd of de gelinkte (via uri) resource nog bestaat.
Voordeel van deze methode is dat je ook gelinkte data van buiten het domein van de organisatie kan controleren.

Een combinatie van de 2 geeft waarschijnlijk de beste resultaten.



Redirect
--------

Het probleem van resources die verwijderd en vervangen worden door andere, moet door de authentieke bron opgelost worden. Een HTTP 301 status code
is hier het correcte antwoord wanneer een iemand deze verwijderde en vervangen resource wil opvragen.



