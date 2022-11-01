# ReadME
# Tento soubor slouží jako diář, do kterého budeme zapisovat různe změny v projektu a veškeré problémy na které jsme narazili a jak se vyřesili


##### #### ZADÁNÍ #### #### ZADÁNÍ #### #### #### ZADÁNÍ #### #### #### ZADÁNÍ #### #### ZADÁNÍ #### 
Vytvořte datové struktury pro definici přítomnosti na události, typu přítomnosti na události,  specifikaci obsahu (stručný popis události, komplexní popis události), specifikaci vyplývajících úkolů.
Úkoly zadané osobám (viz 1.). U úkolů stručný popis, detailní popis, jeden odkaz, datum zadání, datum, kdy má být splněno, datum, kdy bylo splněno  



# ################### 17.10.2022 ######################## #

Tento den se konzultovvalo s prof. Štefkem.

Ujasnili jsme si zadání projekt, jaké máme mít entity, kolik jich bude a co v nich bude.

Abychom mohli pracovat s tímto repo. tak byla potřeba si udělat vlastní kontejner (pojemonován gql_events2).
Do toho kontejneru jsme poté zkopírovali z gql_ug DPDefinitions.py až po GraphTypeDefinitions do našeho kontejneru. 

DPDefinitions.py jsme si upravili podle našeho diagramu. Přidali jsme tam naše 4 entity (PresenceModel, PresenceType, TaskModel a ContentModel).
Po té jsme upravili soubor DPFeeder.py aby souhlasil s naším DPDefinitions.py.

Co se má psát si nejsme úplně jistí, jelikož v tomto prostředí pracujeme poprvé.
Vše se ale ujasní na zítřejším projketovým dnu.

Nebylo to odzkoušeno v Apollu.


# ################### 18.10.2022 ######################## #

Zjistilo se, že kontejner gql_events2 (přejmenován na gql_presence) je špatně nadefinovaný a kontejner Apollo se nespustí. Bez našeho presence kontejneru vše funguje jak má.

Chyběl nám v gql_presence DockerFile, main.py a requiremts. I po přidání nám stále nefungovovali kontejnery. 
Do příštího projektového dnu bude třeba zprovoznit kontejner gql_presence a správně si nadefinovat třídy, funkce, enitity a atributy.

# ################### 1.11.2022 ######################## #

Nově jsme si forkly repo a podle doporučeného postupu jsme pracovali.
Nadefinovali jsme si datové struktury v DBDefinitions.
Po té jsme nadefinovali resolvery v GraphResolvers a na závěr jsme definovali gql modely v GraphTypeDefinitions.

Snažili jsme se pochopit pomocí co vůbec píšeme a jak se to má psát.

Všechny kontejnery fungují a spustil se i postgress, akorát si nejsme jistí jak máme otestovat naši datovou strukturu.

# ################### PRVNÍ KONZULTACE - 17.10.2022 ######################## #

1. Ujasnit si zadání - splněno
2. Co budu potřebovat a v čem se bude pracovat - splněno

ER-Diagram je hotový (zatím)
Je potřeba udělat si vlastní container (např. gql_events2) se kterým budeme pracovat.
Inspiraci můžeme hledat v gql_ug, kde jsou soubory jako DBDefinitions

# #################### PROJEKTOVÝ DEN - 18.10.2022 ############################ #

-udělat schéma - splněno
-github a fork - splněno
-commit v posledních sedmí dní - splněno
-vytvořit kontejner - splněno
-do kontejneru sepsat entity - splněno


# ################### DRUHÉ KONZULTACE 27.10.2022 ##############################

1. Jak vytvořit kontejner - splněno


Je potřeba si udělat nový fork repositáře uosi/v.2.1,  ve kterém je nově udělaná složka gql_empty.
V gql_empty máme stejně soubory jako v qgl_ug, akorát prázdné. Tyto soubory si máme doplnit podle naší potřeby.
Doporučený postup je - Nadefinovat si datové struktury v DBDefinitions. Po té vyplnit GraphResolvers a na závěr GraphTypeDefinitons.
Po vyplnění těchto souborů si máme otestovat funkčnost v postgress, jestli je vše správně nadefinované a naindexované.

Tohle je potřeba udělat do příštího projektového dne.

# ################### TŘETÍ KONZULTACE 1.11.2022 ##############################

1. Co je to resolver
2. Jestli jsou správně napsané
3. Pomoc s GraphTypeDef

# #################### PROJEKTOVÝ DEN - 29.11.2022 ############################ #


# Osoby zodpovědné za tento project

| Person | Role | Project Job | Period |
|:------:|:----:|:-----------:|:------:|
| JR     |STUDENT|     SQL, GQL                     | 2022/9 - 2023/2 |
| KM     |STUDENT|     SQL, GQL                     | 2022/9 - 2023/2 |

