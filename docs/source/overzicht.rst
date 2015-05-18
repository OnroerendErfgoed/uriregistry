=========
Overzicht
=========


We werken steeds meer met verspreide authentieke bronnen. Vroeger zaten veel
van dergelijke bronnen in één databank en was het makkelijk er voor te zorgen
dat een gebruiker geen afhankelijkheden kon wissen. Bv. Een gebruiker wenst
een Actor te wissen uit de lijst van Actoren. Indien deze actor nog de
fotograaf van een bepaalde afbeelding is, wordt dit nu tegengehouden door de
databank omdat er een Foreign Key relatie is.

Eens we een actoren databank en een afbeeldingen databank hebben, is het niet
meer mogelijk om deze controle aan de databank over te laten.

In een typisch REST scenario kunnen we dit ook opvangen door er van uit te gaan
dat de server geen verantwoordelijkheid heeft naar de client om resources
beschikbaar te houden, maar dat legt heel veel verantwoordelijkheid bij de client.
Een andere optie is de resources beschikbaar te houden in een soort "deleted"
versie zodat het altijd mogelijk is te weten wat een bepaalde URI was voor ze
verwijderd werd. Het kan ook nuttig zijn de server zo te programmeren dat deze
een opvolger kan aanduiden. Bv. bij het verwijderen van actor 15 kan dan gesteld
worden dat deze nu vervangen werd door actor 589.

Echter, we beginnen eerst met het zoeken van een manier om te controleren of
een resource nog in gebruik is bij andere resources. Stel:

 * Gebruiker wenst actor 7 te verwijderen. DELETE actoren/7
 * De Actoren service kent een lijst van andere services die actoren kunnen
   gebruiken. De actoren service bevraagt al die andere services om te zien of
   actor 7 ergens in gebruik is.
 * Indien alle services antwoorden dat actor 7 niet in gebruik is, mag de actor
   verwijderd worden.

Te implementeren:

 * Graag zo generiek en uitbreidbaar mogelijk. Een soort register van plugins
   die kunnen controleren of een service aan resource gebruikt. Ofwel is dit
   een klein stukje code in elke toepassing, ofwel een aparte library die we
   inpluggen en configureren.
 * Communicatie is altijd over URI's. Dus, service X vraagt aan service Y of
   deze bv. http://id.erfgoed.net/actoren/7 gebruikt, niet *actor.7* of zo.
 * Elke service biedt de volgende URL aan: */references?uri=<uri>*. Ofwel
   kan deze antwoorden met een lege lijst (wat wil zeggen dat er geen
   referenties naar deze URI zijn). Ofwel kan de service antwoorden met een
   lijst van referenties.
 * Elke referentie heeft de volgende kenmerken:
   * **id:** Id van de resource die de gevraagde URI gebruikt.
   * **uri:** URI naar de resource die de gevraagde URI gebruikt.
   * **omschrijving:** Een korte omschrijving van de resource zoals een titel of
     een naam
 * Ik zou dit liefst ook in Atramhasis willen implementeren. Zodat we bij
   Atramhasis ook een lijst van externe services kunnen opgeven die moeten
   gecontroleerd worden. Lijkt me best om hier een soort plugin te gebruiken
   die standaard de controle doet zoals hierboven beschreven, maar waarbij je
   zelf ook een andere plugin kunt schrijven die bv. een SOAP service bevraagt.