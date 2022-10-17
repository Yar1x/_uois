from doctest import master
from functools import cache
from gql_events2.DBDefinitions import BaseModel, PresenceModel, PresenceType, TaskModel, ContentModel


import random
import itertools
from functools import cache

@cache
def determinePresenceTypes():
    """Definuje zakladni typy pritomnosti a udrzuje je v pameti"""
    presenceTypes = [
        {'name': 'pritomen'},
        {'name': 'nemoc'},

        {'name': 'nahradni volno'},
        {'name': 'sluzebni volno'},
        {'name': 'radna dovolena'},

        {'name': 'sluzba'}
        
        ]
    return presenceTypes

from sqlalchemy.future import select

async def createSystemDataStructurePresenceTypes(asyncSessionMaker):
    """Zabezpeci prvotni inicicalizaci typu roli v databazi"""
    # ocekavane typy roli
    presenceTypes = determinePresenceTypes()
    
    #dotaz do databaze
    stmt = select(PresenceType)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRoleTypes = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbPresenceTypes = [
        {'name': presence.name, 'id': presence.id} for presence in dbPresenceTypes
        ]

    print('presencetypes found in database')
    print(dbPresenceTypes)

    presenceTypeNamesInDatabase = [presenceType['name'] for presenceType in dbPresenceTypes]

    unsavedPresenceTypes = list(filter(lambda presenceType: not(presenceType['name'] in presenceTypeNamesInDatabase), presenceTypes))
    print('presencetypes not found in database')
    print(unsavedPresenceTypes)

    PresenceTypeToAdd = [PresenceType(name = presenceType['name']) for presenceType in unsavedPresenceTypes]
    print(PresenceTypeToAdd)
    print(len(PresenceTypeToAdd))

    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(PresenceTypeToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(PresenceType)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbPresenceTypes = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbPresenceTypes = [
        {'name': presence.name, 'id': presence.id} for presence in dbPresenceTypes
        ]

    print('presencetypes found in database')
    print(dbPresenceTypes)

    presenceTypeNamesInDatabase = [presenceType['name'] for presenceType in dbPresenceTypes]

    unsavedPresenceTypes = list(filter(lambda presenceType: not(presenceType['name'] in presenceTypeNamesInDatabase), presenceTypes))

    # ted by melo byt pole prazdne
    print('presencetypes not found in database')
    print(unsavedPresenceTypes)
    if not(len(unsavedPresenceTypes) == 0):
        print('SOMETHING is REALLY WRONG')

    # a ted maly hack, doplnime IDcka do cache
    for presenceType in presenceTypes:
        presenceTypeName = presenceType['name']
        dbRecords = list(filter(lambda item: (item['name'] == presenceTypeName), dbPresenceTypes))
        assert len(dbRecords) == 1, f'Nalezen {len(dbRecords)} pocet zaznamu :('
        presenceType['id'] = dbRecords[0]['id']

    # test hacku
    print('Role types in database')
    print(determinePresenceTypes())
    pass

