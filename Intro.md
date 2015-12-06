# Temat #

Symulator koewolucji drapieżnik-ofiara.

Celem projektu jest opracowanie sysmulacji pozwalającej obserwować zachodzenie procesu koewolucji - współzależnej ewolucji dwóch lub większej liczby gatunków, z których w każdym zachodzi stopniowe dostosowanie do pozostałych, na zasadzie pewnego rodzaju sprzężenia zwrotnego.

# Założenia podstawowe #

  * Aktorzy: Roślinki, Ofiara, Drapieżnik
  * Łańcuch pokarmowy: Roślinki --> Ofiary --> Drapieżniki

## Roślinki ##
  * statyczne - nie poruszają się
  * w trakcie dnia ilość energii przez nie magazynowana rośnie (fotosynteza)
  * pojawiają się samorzutnie w różnych miejscach planszy (samosiejki)
  * są źródłem energii dla Ofiar

## Ofiary ##
  * poruszają się po mapie - spalając energię
  * czerpią energię ze zjadanych części Roślin
  * są źródłem energii dla Drapieżników - muszą przed nimi uciekać
  * zabite przez Drapieżnika mogą stać się źródłem pożywienia dla innych Drapieżników (statyczne)
  * posiadają zestaw przystosowań, które bezpośrednio wpływają na ich cechy (szybkość, zwrotność, obszar widzenia, itp.) - decydują o ich przetrwaniu
  * gdy czują się nie zagrożone i są syte, mogą się krzyżować
  * jeśli nie będą w stanie zdobyć pożywienia umierają z głodu

## Drapieżniki ##
  * poruszają się po mapie - spalając energię
  * czerpią energię ze zjadanych Ofiar
  * nie muszą się nikogo bać
  * posiadają zestaw przystosowań, które bezpośrednio wpływają na ich cechy (szybkość, zwrotność, obszar widzenia, itp.) - decydują o możliwości upolowania Ofiary
  * gdy są syte mogą się krzyżować
  * jeśli nie będą w stanie zdobyć pożywienia umierają z głodu

## Przystosowania organizmów ##

Każdy organizm posiada wektor liczb określający przystosowania zwierzęcia (w sposób ciągły). Przystosowania decydują o cechach organizmu - są przeliczane na wektor cech reprezentowanych przez liczby.

Przykładowo:

Przystosowania:
  * (1) Długość łap przednich: (a)+0.7, (b)-0.3, (c)+0.4
  * (2) Długość łap tylnych: (a)+1.4, (b)-0.1, (c)+0.4
  * (3) Wielkość uszu: (c)+0.8

Cechy:
  * (a) Szybkość
  * (b) Zwrotność
  * (c) Zdolność zauważania niebezpieczeństwa

Wektor przystosowań: [1.0, 2.0, 3.0]
=>
Wektor cech: TODO

## Krzyżowanie ##

Przy krzyżowaniu powstaje nowy organizm dziedziczący wektor przystosowań po swoich rodzicach.

Wynikowy wektor przystosowań powstaje poprzez:
  * krzyżowanie
  * mutacje