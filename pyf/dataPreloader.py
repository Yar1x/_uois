from functools import cache
from types import MappingProxyType

from models import BaseEntities

def ensureDataItem(session, Model, name):
    itemRecords = session.query(Model).filter(Model.name == name).all()
    itemRecordsLen = len(itemRecords)
    if itemRecordsLen == 0:
        itemRecord = Model(name='department')
        session.add(itemRecord)
        session.commit()
    else:
        assert itemRecordsLen == 1, f'Database has inconsistencies {Model}, {name}'
        itemRecord = itemRecords[0]
    return itemRecord.id

@cache
def ensureData(SessionMaker):
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()
    session = SessionMaker()
    try:
        departmentTypeId = ensureDataItem(session, GroupTypeModel, 'department')
        facultyTypeId = ensureDataItem(session, GroupTypeModel, 'faculty')
        studyGroupId =  ensureDataItem(session, GroupTypeModel, 'studygroup')

        departmentHeadRoleTypeId = ensureDataItem(session, RoleTypeModel, 'head of department')
        deanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'dean')
        viceDeanRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice dean')
        rectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'rector')
        viceRectorRoleTypeId = ensureDataItem(session, RoleTypeModel, 'vice rector')

        result = {
            'departmentTypeId': departmentTypeId,
            'facultyTypeId': facultyTypeId,
            'studyGroupId': studyGroupId,
            'departmentHeadRoleTypeId': departmentHeadRoleTypeId,
            'deanRoleTypeId': deanRoleTypeId,
            'viceDeanRoleTypeId': viceDeanRoleTypeId,
            'rectorRoleTypeId': rectorRoleTypeId,
            'viceRectorRoleTypeId': viceRectorRoleTypeId
        }    
    finally:
        session.close()
    return MappingProxyType(result)


import random
def randomUser(mod='main'):
    surNames = [
        'Novák', 'Nováková', 'Svobodová', 'Svoboda', 'Novotná',
        'Novotný', 'Dvořáková', 'Dvořák', 'Černá', 'Černý', 
        'Procházková', 'Procházka', 'Kučerová', 'Kučera', 'Veselá',
        'Veselý', 'Horáková', 'Krejčí', 'Horák', 'Němcová', 
        'Marková', 'Němec', 'Pokorná', 'Pospíšilová','Marek'
    ]

    names = [
        'Jiří', 'Jan', 'Petr', 'Jana', 'Marie', 'Josef',
        'Pavel', 'Martin', 'Tomáš', 'Jaroslav', 'Eva',
        'Miroslav', 'Hana', 'Anna', 'Zdeněk', 'Václav',
        'Michal', 'František', 'Lenka', 'Kateřina',
        'Lucie', 'Jakub', 'Milan', 'Věra', 'Alena'
    ]

    name1 = random.choice(names)
    name2 = random.choice(names)
    name3 = random.choice(surNames)
    email = f'{name1}.{name2}.{name3}@{mod}.university.world'
    return {'name': f'{name1} {name2}', 'surname': name3, 'email': email}

def preloadData(SessionMaker):
    session = SessionMaker()
    UserModel, GroupModel, RoleModel, GroupTypeModel, RoleTypeModel = BaseEntities.GetModels()
    
    typeIds = ensureData(SessionMaker)
    
    allTeachersGroup = GroupModel(name='teachers')
    allStudentsGroup = GroupModel(name='students')

    session.add(allTeachersGroup)
    session.add(allStudentsGroup)
    session.commit()
    
    def RandomizedStudents(faculty, studyGroup, count=10):
        for _ in range(count):
            student = randomUser(mod=faculty.name)
            studentRecord = UserModel(**student)
            session.add(studentRecord)
            faculty.users.append(studentRecord)
            studyGroup.users.append(studentRecord)
            allStudentsGroup.users.append(studentRecord)
        session.commit()
    
    def RandomizedStudyGroup(faculty):
        name = f"{faculty.name}5-{random.choice([1, 2, 3, 4, 5])}{random.choice(['B', 'C', 'K'])}{random.choice(['A', 'E', 'I'])}"
        studyGroupRecord = GroupModel(name=name, grouptype_id=typeIds['studyGroupId'])
        session.add(studyGroupRecord)
        session.commit()
        RandomizedStudents(faculty, studyGroupRecord, count=random.randint(5, 15))
        pass
    
    def RandomizedTeachers(faculty, department, count=10):
        for _ in range(count):
            teacher = randomUser(mod=faculty.name)
            teacherRecord = UserModel(**teacher)
            session.add(teacherRecord)
            faculty.users.append(teacherRecord)
            department.users.append(teacherRecord)
            allTeachersGroup.users.append(teacherRecord)
        session.commit()
        
    def RandomizedDepartment(faculty, index):
        name = f"{faculty.name}_{index}_{random.choice(['B', 'C', 'K'])}{random.choice(['A', 'E', 'I'])}"
        departmentRecord = GroupModel(name=name, grouptype_id=typeIds['departmentTypeId'])
        session.add(departmentRecord)
        session.commit()
        RandomizedTeachers(faculty, departmentRecord, count=random.randint(5, 20))
        pass
    
    def RandomizedFaculty(index):
        facultyGroup = GroupModel(name=f'F{index}', grouptype_id=typeIds['facultyTypeId'])
        session.add(facultyGroup)
        session.commit()
        departmentCount = random.randrange(4, 14)
        for _ in range(departmentCount):
            RandomizedDepartment(facultyGroup, index=_)
        studyGroupCount = random.randrange(20, 40)
        for _ in range(studyGroupCount):
            RandomizedStudyGroup(facultyGroup)
        session.commit()
    
    def RandomizedUniversity():
        facultyCount = random.randrange(3, 7)
        for index in range(facultyCount):
            RandomizedFaculty(index)
        session.commit()
        
    RandomizedUniversity()
    session.commit()
    session.close()
    

def loadRandomizedData():
    pass

def subjects():
    

    """3D optická digitalizace 1
    Agentní a multiagentní systémy
    Aktuální témata grafického designu
    Algebra
    Algoritmy
    Algoritmy (v angličtině)
    Analogová elektronika 1
    Analogová elektronika 2
    Analogová technika
    Analýza a návrh informačních systémů
    Analýza binárního kódu
    Analýza systémů založená na modelech
    Anglická konverzace na aktuální témata
    Anglická konverzace na aktuální témata
    Angličtina 1: mírně pokročilí 1
    Angličtina 2: mírně pokročilí 2
    Angličtina 3: středně pokročilí 1
    Angličtina 3: středně pokročilí 1
    Angličtina 4: středně pokročilí 2
    Angličtina 4: středně pokročilí 2
    Angličtina pro doktorandy
    Angličtina pro Evropu
    Angličtina pro Evropu
    Angličtina pro IT
    Angličtina pro IT
    Angličtina: praktický kurz obchodní konverzace a prezentace
    Aplikace paralelních počítačů
    Aplikovaná herní studia - výzkum a design
    Aplikované evoluční algoritmy
    Architektura 20. století
    Architektury výpočetních systémů
    Audio elektronika
    Automatizované testování a dynamická analýza
    Autorská práva - letní
    Bakalářská práce
    Bakalářská práce Erasmus (v angličtině)
    Bayesovské modely pro strojové učení (v angličtině)
    Bezdrátové a mobilní sítě
    Bezpečná zařízení
    Bezpečnost a počítačové sítě
    Bezpečnost informačních systémů
    Bezpečnost informačních systémů a kryptografie
    Bioinformatika
    Bioinformatika
    Biologií inspirované počítače
    Biometrické systémy
    Biometrické systémy (v angličtině)
    Blockchainy a decentralizované aplikace
    CCNA Kybernetická bezpečnost (v angličtině)
    České umění 1. poloviny 20. století v souvislostech - zimní
    České umění 2. poloviny 20. století v souvislostech - letní
    Chemoinformatika
    Číslicové zpracování akustických signálů
    Číslicové zpracování signálů (v angličtině)
    CNC obrábění / Roboti v umělecké praxi
    Daňový systém ČR
    Databázové systémy
    Databázové systémy (v angličtině)
    Dějiny a filozofie techniky
    Dějiny a kontexty fotografie 1
    Dějiny a kontexty fotografie 2
    Dějiny designu 1 - letní
    Dějiny designu 1 - zimní
    Desktop systémy Microsoft Windows
    Digitální forenzní analýza (v angličtině)
    Digitální marketing a sociální média (v angličtině)
    Digitální sochařství - 3D tisk 1
    Digitální sochařství - 3D tisk 2
    Diplomová práce
    Diplomová práce (v angličtině)
    Diplomová práce Erasmus (v angličtině)
    Diskrétní matematika
    Dynamické jazyky
    Ekonomie informačních produktů
    Elektroakustika 1
    Elektronický obchod (v angličtině)
    Elektronika pro informační technologie
    Elektrotechnický seminář
    Evoluční a neurální hardware
    Evoluční výpočetní techniky
    Filozofie a kultura
    Finanční analýza
    Finanční management pro informatiky
    Finanční trhy
    Formální analýza programů
    Formální jazyky a překladače
    Formální jazyky a překladače (v angličtině)
    Funkcionální a logické programování
    Funkční verifikace číslicových systémů
    Fyzika 1 - fyzika pro audio inženýrství
    Fyzika v elektrotechnice (v angličtině)
    Fyzikální optika
    Fyzikální optika (v angličtině)
    Fyzikální seminář
    Grafická a zvuková rozhraní a normy
    Grafická uživatelská rozhraní v Javě
    Grafická uživatelská rozhraní v Javě (v angličtině)
    Grafická uživatelská rozhraní v X Window
    Grafické a multimediální procesory
    Grafové algoritmy
    Grafové algoritmy (v angličtině)
    Hardware/Software Codesign
    Hardware/Software Codesign (v angličtině)
    Herní studia
    Informační systémy
    Informační výchova a gramotnost
    Inteligentní systémy
    Inteligentní systémy
    Internetové aplikace
    Inženýrská pedagogika a didaktika
    Inženýrská pedagogika a didaktika
    Jazyk C
    Klasifikace a rozpoznávání
    Kódování a komprese dat
    Komunikační systémy pro IoT
    Konvoluční neuronové sítě
    Kritická analýza digitálních her
    Kruhové konzultace
    Kryptografie
    Kultura projevu a tvorba textů
    Kultura projevu a tvorba textů
    Kurz pornostudií
    Lineární algebra
    Lineární algebra
    Logika
    Makroekonomie
    Management
    Management projektů
    Manažerská komunikace a prezentace
    Manažerská komunikace a prezentace
    Manažerské vedení lidí a řízení času
    Manažerské vedení lidí a řízení času
    Matematická analýza 1
    Matematická analýza 2
    Matematická logika
    Matematické struktury v informatice (v angličtině)
    Matematické výpočty pomocí MAPLE
    Matematické základy fuzzy logiky
    Matematický seminář
    Matematický software
    Matematika 2
    Maticový a tenzorový počet
    Mechanika a akustika
    Mikroekonomie
    Mikroprocesorové a vestavěné systémy
    Mikroprocesorové a vestavěné systémy (v angličtině)
    Mobilní roboty
    Modelování a simulace
    Modelování a simulace
    Moderní matematické metody v informatice
    Moderní metody zobrazování 3D scény
    Moderní metody zpracování řeči
    Moderní teoretická informatika
    Moderní trendy informatiky (v angličtině)
    Molekulární biologie
    Molekulární genetika
    Multimédia
    Multimédia (v angličtině)
    Multimédia v počítačových sítích
    Návrh a implementace IT služeb
    Návrh a realizace elektronických přístrojů
    Návrh číslicových systémů
    Návrh číslicových systémů (v angličtině)
    Návrh kyberfyzikálních systémů (v angličtině)
    Návrh počítačových systémů
    Návrh vestavěných systémů
    Návrh, správa a bezpečnost
    Operační systémy
    Optické sítě
    Optika
    Optimalizace
    Optimalizační metody a teorie hromadné obsluhy
    Optimální řízení a identifikace
    Paralelní a distribuované algoritmy
    Paralelní výpočty na GPU
    Pedagogická psychologie
    Pedagogická psychologie
    Plošné spoje a povrchová montáž
    Počítačová fyzika I
    Počítačová fyzika II
    Počítačová grafika
    Počítačová grafika
    Počítačová grafika (v angličtině)
    Počítačová podpora konstruování
    Počítačové komunikace a sítě
    Počítačové vidění (v angličtině)
    Počítačový seminář
    Podnikatelská laboratoř
    Podnikatelské minimum
    Pokročilá bioinformatika
    Pokročilá matematika
    Pokročilá počítačová grafika (v angličtině)
    Pokročilá témata administrace operačního systému Linux
    Pokročilé asemblery
    Pokročilé biometrické systémy
    Pokročilé číslicové systémy
    Pokročilé databázové systémy
    Pokročilé databázové systémy (v angličtině)
    Pokročilé informační systémy
    Pokročilé komunikační systémy (v angličtině)
    Pokročilé operační systémy
    Pokročilé směrování v páteřních sítích (ENARSI)
    Pokročilé techniky návrhu číslicových systémů
    Pokročilý návrh a zabezpečení podnikových sítí
    Praktické aspekty vývoje software
    Praktické paralelní programování
    Pravděpodobnost a statistika
    Právní minimum
    Právní minimum
    Právo informačních systémů
    Přenos dat, počítačové sítě a protokoly
    Přenos dat, počítačové sítě a protokoly (v angličtině)
    Principy a návrh IoT systémů
    Principy programovacích jazyků a OOP
    Principy programovacích jazyků a OOP (v angličtině)
    Principy syntézy testovatelných obvodů
    Programovací seminář
    Programování na strojové úrovni
    Programování v .NET a C#
    Programování zařízení Apple
    Projektová praxe 1
    Projektová praxe 1
    Projektová praxe 1 (v angličtině)
    Projektová praxe 1 (v angličtině)
    Projektová praxe 1 (v angličtině)
    Projektová praxe 1 (v angličtině)
    Projektová praxe 2
    Projektová praxe 2
    Projektová praxe 2 (v angličtině)
    Projektová praxe 2 (v angličtině)
    Projektová praxe 3
    Projektování datových sítí
    Projektový manažer
    Prostředí distribuovaných aplikací
    Rádiová komunikace
    Regulované gramatiky a automaty
    Rétorika
    Rétorika
    Řízení a regulace 1
    Řízení a regulace 2
    Robotika (v angličtině)
    Robotika a manipulátory
    Robotika a zpracování obrazu
    Semestrální projekt
    Semestrální projekt
    Semestrální projekt (v angličtině)
    Semestrální projekt Erasmus (v angličtině)
    Semestrální projekt Erasmus (v angličtině)
    Seminář C#
    Seminář C++
    Seminář diskrétní matematiky a logiky
    Seminář Java
    Seminář Java (v angličtině)
    Seminář VHDL
    Senzory a měření
    Serverové systémy Microsoft Windows
    Signály a systémy
    Simulační nástroje a techniky
    Síťová kabeláž a směrování (CCNA1+CCNA2)
    Síťové aplikace a správa sítí
    Skriptovací jazyky
    Složitost (v angličtině)
    Směrování a přepínání v páteřních sítích (ENCOR)
    Soft Computing
    Španělština: začátečníci 1/2
    Španělština: začátečníci 2/2
    Správa serverů IBM zSeries
    Statická analýza a verifikace
    Statistika a pravděpodobnost
    Statistika, stochastické procesy, operační výzkum
    Strategické řízení informačních systémů
    Strojové učení a rozpoznávání
    Systémová biologie
    Systémy odolné proti poruchám
    Systémy odolné proti poruchám
    Systémy pracující v reálném čase (v angličtině)
    Technologie sítí LAN a WAN (CCNA3+4)
    Teoretická informatika
    Teoretická informatika (v angličtině)
    Teorie a aplikace Petriho sítí
    Teorie her
    Teorie kategorií v informatice
    Teorie programovacích jazyků
    Testování a dynamická analýza
    Tvorba aplikací pro mobilní zařízení (v angličtině)
    Tvorba uživatelských rozhraní
    Tvorba uživatelských rozhraní (v angličtině)
    Tvorba webových stránek
    Tvorba webových stránek (v angličtině)
    Typografie a publikování
    Účetnictví
    Ukládání a příprava dat
    Umělá inteligence a strojové učení
    Úvod do molekulární biologie a genetiky
    Úvod do softwarového inženýrství
    Uživatelská zkušenost a návrh rozhraní a služeb (v angličtině)
    Vědecké publikování od A do Z
    Vizualizace a CAD (v angličtině)
    Vizuální styly digitálních her 1
    Vizuální styly digitálních her 2
    Vybraná témata z analýzy a překladu jazyků
    Vybrané kapitoly z matematiky
    Vybrané partie z matematiky I.
    Vybrané partie z matematiky II.
    Vybrané problémy informačních systémů
    Výpočetní fotografie
    Výpočetní geometrie
    Výpočetní geometrie (v angličtině)
    Vysoce náročné výpočty
    Vysoce náročné výpočty
    Vysoce náročné výpočty (v angličtině)
    Výstavba překladačů (v angličtině)
    Výtvarná informatika
    Zabezpečovací systémy
    Zahraniční odborná praxe
    Zahraniční odborná praxe
    Základy ekonomiky podniku
    Základy financování
    Základy herního vývoje
    Základy hudební akustiky
    Základy marketingu
    Základy počítačové grafiky
    Základy programování
    Základy umělé inteligence
    Základy umělé inteligence (v angličtině)
    Získávání znalostí z databází
    Zkouška z jazyka anglického pro Ph.D.
    Zobrazovací systémy v lékařství
    Zpracování a vizualizace dat v prostředí Python
    Zpracování obrazu
    Zpracování obrazu (v angličtině)
    Zpracování přirozeného jazyka
    Zpracování přirozeného jazyka (v angličtině)
    Zpracování řeči a audia člověkem a počítačem
    Zpracování řečových signálů
    Zpracování řečových signálů (v angličtině)
    Zvukový software"""
    
    
    pass