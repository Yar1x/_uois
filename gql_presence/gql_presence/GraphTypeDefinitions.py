from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#
from gql_presence.GraphResolvers import resolvePresenceModelPage, resolvePresenceModelById
from gql_presence.GraphResolvers import resolvePresenceTypeModelPage,resolvePresenceTypeModelById
from gql_presence.GraphResolvers import resolvePresenceTypeForPresence
from gql_presence.GraphResolvers import resolveTaskOnEventModelPage, resolveTaskOnEventModelById
from gql_presence.GraphResolvers import resolveTaskModelByPage, resolveTaskModelById
from gql_presence.GraphResolvers import resolveContentModelByPage, resolveContentModelById


@strawberryA.federation.type(keys=["id"], description="""Entity representing presence""")
class PresenceGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePresenceModelById (AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    #změna pro foreign key
    # jiný resolver PresencemodelTypebyId
    # vztah N ku 1
    @strawberryA.field(description="""PresenceTypeId""")
    async def presence_type(self, info: strawberryA.types.Info) -> 'PresenceTypeGQLModel':
        result = await resolvePresenceTypeModelById(AsyncSessionFromInfo(info), self.presenceType_id)
        return result

    @strawberryA.field(description="""user id""")
    def user_id(self) -> 'UserGQLModel':
       return self.user_id

    
    @strawberryA.field(description="""Task on event Id""")
    async def task_on_event(self) -> 'TaskOnEventGQLModel':
        return self.task_on_event
   
@strawberryA.federation.type(keys=["id"], description="""Entity representing presence type""")
class PresenceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePresenceTypeModelById (AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Presence type name (absent/present)""")
    def type(self) -> str:
        return self.type

    @strawberryA.field(description="""PresenceId""")
    async def presence(self) -> 'PresenceGQLModel':
        return self.presence
    
@strawberryA.federation.type(keys=["id"], description="""Entity for Tasks on events""")
class TaskOnEventGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveTaskOnEventModelById (AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result

    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
        
    @strawberryA.field(description="""PresenceId""")
    async def presence(self) -> 'PresenceGQLModel':
        return self.presence

    @strawberryA.field(description="""Task Id""")
    async def presence(self) -> 'TaskGQLModel':
        return self.presence   
        

@strawberryA.federation.type(keys=["id"], description="""Entity representing tasks""")
class TaskGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id:strawberryA.ID):
        result = await resolveTaskModelById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result

    #co se vrací bude atributem (přímo v tabulce)
    #           relace (v jiné tabulce) -> udělat resolver viz ř. 44
    @strawberryA.field(description="""Primary key of task""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""TaskOnEvent Id""")
    async def presence(self) -> 'TaskOnEventGQLModel':
        return self.presence
    
    @strawberryA.field(description="""user Id""")
    async def presence(self) -> 'UserGQLModel':
        return self.presence

@strawberryA.federation.type(keys=["id"], description="""Entity representing content""")
class ContentGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id:strawberryA.ID):
        result = await resolveContentModelById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""Primary key of content""")
    def id(self) -> strawberryA.ID:
        return self.id 

   # @strawberryA.field(description="""Event Id""")
   # async def presence(self) -> 'EventGQLModel':
   #     return self.presence
    
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    
    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id) # jestlize rozsirujete, musi byt tento vyraz
    
    # výstup list pro typu přítomnosti uživatele
    # -> List[...]
    # async def ...
    # (self, info: strawberryA ....)
    # v těle volat resolver PresenceForUser (create1NGetter)
    @strawberryA.field(description="""presence id""")
    def presence(self) -> 'PresenceGQLModel':
       return self.presence
       
    
    
    
#     zde je rozsireni o dalsi resolvery¨
#     async def external_ids(self, info: strawberryA.types.Info) -> List['ExternalIdGQLModel']:
#         result = await resolveExternalIds(AsyncSessionFromInfo(info), self.id)
#         return result


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

@strawberryA.type(description="""Type for query root""")
class Query:
   # nedotazovat se na TaskOnEventModel
    @strawberryA.field(description="""Finds a workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds presence by their id""")
    async def presence_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PresenceGQLModel, None]:
        result = await resolvePresenceModelById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds presence by their page""")
    async def presence_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PresenceGQLModel]:
        result = await resolvePresenceModelPage(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Finds presence type by their id""")
    async def presence_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[PresenceTypeGQLModel, None]:
        result = await resolvePresenceTypeModelById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds presence by their page""")
    async def presence_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PresenceTypeGQLModel]:
        result = await resolvePresenceTypeModelPage(AsyncSessionFromInfo(info), skip, limit)
        return result
    
    @strawberryA.field(description="""Finds tasks by their id""")
    async def task_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[TaskGQLModel, None]:
        result = await resolveTaskModelById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds tasks by their page""")
    async def task_page(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[TaskGQLModel, None]:
        result = await resolveTaskModelByPage(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Finds content by their id""")
    async def content_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ContentGQLModel, None]:
        result = await resolveContentModelById(AsyncSessionFromInfo(info), id)
        return result
    
    @strawberryA.field(description="""Finds content by their page""")
    async def content_page(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ContentGQLModel, None]:
        result = await resolveContentModelByPage(AsyncSessionFromInfo(info), id)
        return result

    #radnomPresenceData 
    #async def ....
    #zavolat funkci 
    #předat výstup výsledku dotazu
    #vrátit hlavní datovou strukturu
    #resolvePresenceModelById

    



    

    
###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))