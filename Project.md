# Diagram klas #

![http://evolv.googlecode.com/svn/trunk/doc/images/classdiagram.png](http://evolv.googlecode.com/svn/trunk/doc/images/classdiagram.png)

# Modelowane klasy #

## Agenci statyczni ##
  * **Plant** ([analiza](http://code.google.com/p/evolv/wiki/Intro#Roślinki)) - Pierwsze ogniwo łańcucha pokarmowego
    * energy

## Agenci mobilni ##
  * **Rabbit** ([analiza](http://code.google.com/p/evolv/wiki/Intro#Ofiary)) - Ofiary
  * **Wolf** ([analiza](http://code.google.com/p/evolv/wiki/Intro#Drapieżniki)) - Drapieżniki

  * **Animal** - Klasa bazowa
    * energy
    * health
    * age

## Cechy i przystosowania ##
  * **Anatomy** - genotyp, cechy fizyczne zwierząt (klasa: Animal)
    * size
    * ears
    * legs
    * tail
    * teeth
    * fur
    * eyes
    * pregnancy
    * stomach
    * muzzle

  * **Abilities** - fenotyp, zdolności zwierząt mające bezpośredni wpływ na ich przetrwanie
    * speed
    * agility
    * observation
    * camouflage
    * urge
    * digestion
    * effectiveness

> Analiza: [link](http://code.google.com/p/evolv/wiki/Intro#Przystosowania_organizmów)

## Środowisko życia organizmów ##
  * **Environment** - Kontroler animacji, reprezentacja świata symulacji
  * **Tree**, **Meadow** (**Terrain**) - Obszar na mapie mający wpływ na zdolności zwierząt


# Algorytmy #

## Krzyżowanie organizmów ##

![http://evolv.googlecode.com/svn/trunk/doc/images/genetics.png](http://evolv.googlecode.com/svn/trunk/doc/images/genetics.png)

### Crossover ###
  * n-point crossover - przecięcie genotypu w n losowych miejscach
  * uniform crossover - losowy dobór genotypu od rodziców
  * arithmetic crossover  - wyliczenie genotypu na podstawie genotypów rodziców

### Mutation ###
  * arithmetic - zmiana wartości genotypu za pomocą losowej operacji arytmetycznej
  * random - zmiana wartości genotypu na inna wartość losową