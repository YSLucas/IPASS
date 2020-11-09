# League of Legends MCTS drafter
Door Lucas Siekkötter

## Wat is League of Legends (LoL)
League of Legends is een populaire computer game waarbij 10 spelers verdeeld in 2 teams tegens elkaar spelen. Elke speler speelt met een zelf gekozen champion (in-game character). Welke champion je kiest kan een grote invloed zijn op de uitkomst van het spel, vooral op hoger niveau. De fase waar je je champion keuze maakt is dan ook een belangerijke onderdeel van het spel. Deze fase heet de Draft. Beide teams mogen om en om één champion kiezen.

## Wat is MCTS drafter?
MCTS drafter is een programma dat zich focussed op de Draft. Met het MCTS UCT algoritme probeert deze applicatie de beste champion te kiezen op het moment dat er om gevraagd wordt, en neemt de eerder gekozen champions mee in deze beslissing. Met MCTS drafter speel je tegen het algoritme. Maar tijdens jouw beurt krijg je ook een suggestie over wat het algoritme denk welke champion jij het beste kunt kiezen.

## Start applicatie
Run `Play_draft.py` om de applicatie te starten.

## Data
Er waren een aantal dingen die ik nodig had in de data om een model te kunnen trainen:
* Champions team blauw
* Champions team rood
* Uitkomst van betreffende game (gewonnen / verloren)
* MMR van betreffende game (niveau van spelers)

Om de data te verzamelen heb ik python package `scrapy` gebruikt met de code van https://github.com/MarcusDEFGH/loldraft. De site waar de data vandaan komt is op.gg. De code had nog wel bugs en moest aangepast worden aangezien de data die ik kreeg niet correct was.

Het model dat word gebruik is getraind met data van 9-8 t/m 14-8 en bestaat uit 90.000 unieke matches en is over 5 dagen verzamelt. Je kan `loldb --> spiders --> op.gg.py` runnen om nieuwe data te krijgen. Die data haal je vervolgens door `Data_cleaner.py` om dubbele waardes eruit te halen en het aantal wins van blue en red gelijk te maken.