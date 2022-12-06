# Fasten your seatbelts
![image](assets/images/printlogo.png)
### Concept logo
![image](assets/images/conceptlogo.png)
Dit was ons eerste logo Idee: een robot met een airhockey pusher op zijn hoofd. We hebben ook een naam bedacht: Rob! Dat is een afkorting van ROBot. We zijn dit logo daarna gaan uitwerken en uiteindelijk is het ons uiteindelijke logo geworden:
![image](assets/images/printlogo.png)

## Inleiding
In deze git vind je alles wat nodig is om een airhockey tafel te maken. Dit project is een onderdeel van de studie Techtnische Informatica op de HVA. Dit project is gemaakt door de volgende eerste jaars TI studenten: Koen Lammers, Melvin Moes, Jayden van Oorschot, Simmon Zweers, Nick schokker en Jurrien Simmons.

## Descriptie
Het doel van het project is om een airhockey tafel te maken die werkend is met maar 1 deelnemer. U zal dan spelen tegen een automatische tegenstander die de puck terug zal kaatsen. De benodigdheden kunt u hieronder zien. Het prototype die gemaakt is, is een verkleind versie van onze echte visie. Dus de lijst zal in de realiteit wel kunnen variëren.

## Benodigdheden
- 1x Odroid N2+
- 1x Servo SG90
- 1x Afstand Sensor HC-SR04
- 2x LDR and laser
- 1x Sound sensor
- 1x Segment display
- 1x Airhockey tafel
- 1x Diverse 3d geprinte onderdelen

## Visuals
> Hier onder is een animatie te zien van hoe het product er ongeveer uit moet gaan zien.
![Ontwerp Eindproduct.gif](./Ontwerp Eindproduct.gif)
> Hier onder is te zien hoe het prototype er in realiteit uit ziet.


## Installation
- Fetch uitleg
- Threading uitleg
- Bekabeling Uitleg
- Database
- Git documentatie
- Webserver uitleg
- Technisch ontwerp
- Gebruik

## Support
Voor technische support kunt u altijd support vragen bij een van onze projectdeelnemers. Zie autheuren voor contact informatie.

## Authors
- Koen Lammers        -   koen.lammers@hva.nl
- Melvin Moes         -   melvin.moes@hva.nl
- Jayden van Oorschot -   jayden.vanoorschot@hva.nl
- Nick Schokker       -   nick.schokker@hva.nl
- Simon Zweers        -   simon.zweers@hva.nl
- Jurrrien Simmons    -   jurrien.simmons@hva.nl


## Bronnen
- Database Flask
https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d
- Database Flask
https://www.instructables.com/From-Data-to-Graph-a-Web-Jorney-With-Flask-and-SQL/

## Documentatie Database
<b> Documentatie voor de aangemaakte database.

#    Stap 1.
    sudo apt update //   Dit refresh apt zodat de source list up to date is

#    Stap 2 –
    sudo apt install mysql-server //    Dit installeerd MYSQL op het systeem. Om vervolgens de MYSQL status te verkrijgen voer je “sudo systemctl status mysql” in.

#    Stap 3-
    sudo mysql_secure_installation //   Dit zorgt ervoor dat MYSQL word beveiligd met een wac-htwoord.
     Hierin volgen een aantal stappen:
-    Yes wanneer er word gevraagt om wachtwoord validatie.
-    LOW (0) Wanneer er word gevraagd om welke niveau van wachtwoord validatie.
     Gebruikte password : odroid  

#    Stap 4-
    mysql -u root -p //     Hiermee log je in met root rechten in MYSQL

#    Stap 5-
        1.	CREATE DATABASE sensoren; // Creeerd een database ‘sensoren’
        2.	CREATE USER 'admin'@'localhost' IDENTIFIED by ‘odroid123’;  // Creeerd een gebruiker ‘admin’ met als wachtwoord odroid123. Hiermee      loggen we in later in PHPMYADMIN
        3.	GRANT ALL on sensoren.* to 'admin'@'localhost'; //  Dit geeft account admin volledige rechten over de database sensoren.
        4.	flush privileges //  Dit zorgt ervoor dat alles wat we zojuist hebben aangepast word verwerkt in de server.


