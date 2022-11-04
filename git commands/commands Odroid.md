# Fasten your seatbelts

## Inleiding
Hier vind je de commands voor git op de odroid. Je kan deze commands gebruiken om
git gelijk op de odroid te laten werken in plaats van eerst de files te moeten verplaatsen
naar je computer.

Met clone kan je alles van git op je computer zetten.
## Clone

    git clone

## Pull

    git pull

Git pull zorgt er voor de je de meest up to date versie hebt van de git bestanden.

    git pull origin <name>

Pullt changes van een remote repository.
## Branches

    git branch -a

Git branch laat een lijst zien met alle branches.

    git branch <name>

Git branch maakt een nieuwe branch aan.

    git branch -d <name>

Git branch -d delete de branch.  

    git checkout <name>

Switched naar een branch

    git checkout -b <name>

Maakt een nieuwe branch en switch daar gelijk naar.
## Commit
Om te commiten moet je eerst een branch uploaden in gitlab en vervolgens een merge request
aan maken. Deze moet dan geaccepteerd worden door een ander om zeker te zijn dat de code
is gecontrolleerd.

## SSH key krijgen
Genereert de key

    ssh-keygen
    
    klik enter meerdere keren geef het geen wachtwoord

## Push

    git push
