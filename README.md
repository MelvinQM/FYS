# Fasten your seatbelts

![image](assets/images/printlogo.png)

## Concept logo

![image](assets/images/conceptlogo.png)
Dit was ons eerste logo Idee: een robot met een airhockey pusher op zijn hoofd. We hebben ook een naam bedacht: Rob! Dat is een afkorting van ROBot. We zijn dit logo daarna gaan uitwerken en uiteindelijk is het ons uiteindelijke logo geworden:
![image](assets/images/printlogo.png)

## Inleiding

In deze git vind je alles wat nodig is om ons idee voor een airhockey tafel na te maken. Dit project is een onderdeel van de studie Techtnische Informatica op de HVA. Dit project is gemaakt door de volgende eerste jaars TI studenten: Koen Lammers, Melvin Moes, Jayden van Oorschot, Simon Zweers, Nick schokker en Jurrien Simmons.

## Beschrijving

Het doel van het project is om een airhockey tafel te maken die werkt met maar 1 deelnemer. Je kan dan spelen tegen een automatische tegenstander die de puck terug zal kaatsen. De benodigdheden kan je hieronder zien. Het prototype dat gemaakt is, is een verkleinde versie van onze echte visie. Dus de lijst zal in de realiteit wel kunnen variëren.

## Benodigdheden

- 1x Odroid N2+
- 1x Servo SG90
- 1x Afstand Sensor HC-SR04
- 2x LDR and laser
- 1x Sound sensor
- 1x Segment display
- 1x Airhockey tafel
- 1x Diverse 3d geprinte onderdelen

## Beeldmateriaal

> Hieronder is een animatie te zien van hoe het product er ongeveer uit moet gaan zien.
![Ontwerp Eindproduct.gif](./Ontwerp Eindproduct.gif)
> Hieronder is te zien hoe het prototype er in realiteit uit ziet.
> Hieronder is het aansluitschema te zien. Dit is hoe we alle onderdelen aan de Odroid hebben aangesloten.
![image](assets/images/aansluitschema.png)

## Installatie

- Fetch uitleg
- Threading uitleg
- Bekabeling Uitleg
- Database
- Git documentatie
- Webserver uitleg
- Technisch ontwerp
- Gebruik

## Functies

Om de verschillende onderdelen en sensoren aan te sturen of af te lezen hebben we voor elk onderdeel een aparte functie aangemaakt, die we later allemaal samen kunnen voegen in één bestand.

### Countdown

De eerste functie is voor het aftellen van de tijd tijdens het spelen en het printen van de timer.

```python
# Countdown for the gameloop
def countdown():
    global gameCountdown
    while gameCountdown:
        mins, secs = divmod(gameCountdown, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r")
        time.sleep(1)
        gameCountdown -= 1
        print(timer)
```

Deze functie telt af van 60, elke seconde -1. De timer wordt geprint in het formaat (minuten:seconden).

### Soundsensor

Deze functie is voor de geluidssensor/soundsensor, om het omgevingsgeluid te meten tijdens het spelen.

```python
# Function for usage of Sound Sensor
def soundsensor():
    while True:
        global sound
        # analogRead leest een float value van de sensor af (Geluid dus)
        sound = wpi.analogRead(soundSensor_PIN)
        print("Sound value:", sound)
        # Vergelijk het gelezen value met een preset value die je kan instellen bij oldSound
        if sound > thresholdSound:
            wpi.digitalWrite(LED_PIN, wpi.HIGH)
            print("Threshold Exceeded")
        else:
            wpi.digitalWrite(LED_PIN, wpi.LOW)
            print("Below Threshold")
        time.sleep(soundDelay)
```

De soundsensor geeft een waarde terug, hoe hoger de waarde hoe meer geluid hij opvangt. We blijven deze waarde om de zo veel tijd (soundDelay) opvragen en we vergelijken hem elke keer met de vooraf bepaalde grens (thresholdSound). Als het geluid boven de grens komt, gaat er een led branden.

soundSensor_PIN, thresholdSound en soundDelay zijn buiten deze functie al gedefiniëerd.

### Servo

Deze functie is voor het aansturen van de servo, die de arm laat bewegen.

```python
# Function for usage of servo
def servomovement():
    global gameCountdown
    killTimer = gameCountdown
    # Start program at 90 degrees
    wpi.pwmWrite(servoPin, resetMove)
    while killTimer > 0:
            move = random.randint(int((minMove / 18) + 2) * 45, int((maxMove / 18) + 2) * 45)
            wpi.pwmWrite(servoPin, int(move))
            time.sleep(servoDelay)
            killTimer -= 0.5
    # End program on 90
    wpi.pwmWrite(servoPin, resetMove)
```

Deze functie blijft doorgaan zolang de timer uit de eerste functie nog geen 0 is. De functie berekent de variabele move, dit is een random getal tussen minMove en maxMove (die buiten de functie gedefiniëerd zijn). Zo kunnen we de servo tussen 2 hoeken laten bewegen, bijvoorbeeld 0 en 180.

Als de timer om is wordt de servo teruggezet in het midden.

### LDR

Deze functie is voor de LDR/lichtsensor die we gebruiken om doelpunten te detecteren.

```python
# Function for usage of ldr
def ldr_func():
    while True:
        global LDR_PIN
        # Variabele
        output = wpi.digitalRead(LDR_PIN)
        """
        outputOld = 0
        # print(output, outputOld)
        if output > outputOld:
            print("Lichtje Uit")
        elif output < outputOld:
            print("Lichtje Aan")
        """
        print(output)
        outputOld = output
        time.sleep(ldrDelay)
```

Deze functie leest de waarde van de LDR op de LDR_PIN en vergelijkt deze met de vorige waarde. De LDR is een variabele weerstand, de output wordt hoger als er licht op schijnt. Door de output te vergelijken kunnen we aflezen of er wel of geen licht op schijnt, dus of de laser onderbroken wordt.

### Ultrasonic

Deze functie wordt gebruikt om de afstand te meten met de ultrasonic sensor. 

```python
# Function for usage of ultrasonic
def ultrasonic():
    while True:
        # dist is a variable made for distance()
        # set Trigger to HIGH
        wpi.digitalWrite(triggerPin, wpi.HIGH)

        # set Trigger after 0.01ms to LOW
        time.sleep(ultraSoundDelay)
        wpi.digitalWrite(triggerPin, wpi.LOW)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while wpi.digitalRead(echoPin) == 0:
            StartTime = time.time()

        # save time of arrival
        while wpi.digitalRead(echoPin) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        # if statement that tells if distance is smaller than 100cm lights turn on
        if distance <= 100:
            wpi.digitalWrite(ultraLedStrip, wpi.HIGH)
        # else statements that tells if distance is larger than 100 cm light turn off
        else:
            wpi.digitalWrite(ultraLedStrip, wpi.LOW)

        print("Measured Distance = %.1f cm" % distance)
        time.sleep(1)
```

De ultrasonic sensor kan afstand meten door pulsen van geluid uit te zenden en de tijd meten voor ze terugkomen. Door de triggerPin een kort signaal te geven wordt er een puls van geluid uitgezonden. Wanneer de echoPin een signaal ontvangt wordt de eindtijd opgeslagen. De tijd die voorbij ging is de starttijd - eindtijd. Met de geluidssnelheid (343 m/s) wordt dan de afstand berekend.

Uiteindelijk gaan de lichten branden als de afstand minder is dan onze vastgestelde grens.

## Threading

Wij gebruiken threads in ons project om verschillende sensoren en motoren tegelijk aan te sturen/uit te lezen. Hieronder maken wij deze threads aan. De target voor deze threads zijn de hierboven beschreven functies.

```python
# Making the threads
countdownThread = threading.Thread(target=countdown)
soundThread = threading.Thread(target=soundsensor)
servoThread = threading.Thread(target=servomovement)
ldrThread = threading.Thread(target=ldr_func)
ultraSonicThread = threading.Thread(target=ultrasonic)
```

Nadat de threads zijn aangemaakt worden de threads gestart. Wat dit eigenlijk betekent is dat er aparte stukken code runnen naast de main code. Hierdoor kunnen wij meerdere codes met bijvoorbeeld verschillende delays toevoegen, wat niet mogelijk zou zijn zonder threading.

```python
# Starting the threading
countdownThread.start()
soundThread.start()
servoThread.start()
ldrThread.start()
ultraSonicThread.start()
```

## Documentatie Database

### MYSQL installatie

1. *sudo apt update* // Dit refresh apt zodat de source list up to date is.
2. sudo apt install mysql-server // Dit installeerd MYSQL op het systeem. Om vervolgens de MYSQL status te verkrijgen voer je “sudo systemctl status mysql” in.
3. sudo mysql_secure_installation / /Dit zorgt ervoor dat MYSQL word beveiligd met een wac-htwoord. Hierin volgen een aantal stappen:
Yes wanneer er word gevraagt om wachtwoord validatie.
LOW (0) Wanneer er word gevraagd om welke niveau van wachtwoord validatie.
Gebruikte password : odroid
4. mysql -u root -p //Hiermee log je in met root rechten in MYSQL
5.  
    - CREATE DATABASE sensoren; // Creeerd een database ‘sensoren’
    - CREATE USER 'admin'@'localhost' IDENTIFIED by ‘odroid123’;  // Creeerd een gebruiker ‘admin’ met als wachtwoord odroid123. Hiermee loggen we in later in PHPMYADMIN
    - GRANT ALL on sensoren.* to 'admin'@'localhost';  //Dit geeft account admin volledige rechten over de database sensoren.
    - flush privileges  //Dit zorgt ervoor dat alles wat we zojuist hebben aangepast word verwerkt in de server.

## Support

Voor technische support kun je altijd support vragen bij een van onze projectdeelnemers. Zie autheuren voor contact informatie.

## Authors

- Koen Lammers        -   koen.lammers@hva.nl
- Melvin Moes         -   melvin.moes@hva.nl
- Jayden van Oorschot -   jayden.van.oorschot@hva.nl
- Nick Schokker       -   nick.schokker@hva.nl
- Simon Zweers        -   simon.zweers@hva.nl
- Jurrrien Simmons    -   jurrien.simmons@hva.nl

## Bronnen

- [Database Flask bron #1](https://towardsdatascience.com/python-webserver-with-flask-and-raspberry-pi-398423cc6f5d)
- [Database Flask bron #2](https://www.instructables.com/From-Data-to-Graph-a-Web-Jorney-With-Flask-and-SQL/)
