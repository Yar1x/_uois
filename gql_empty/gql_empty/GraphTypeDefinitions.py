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



from gql_empty.GraphResolvers import resolvePresenceTypeByID
@strawberryA.federation.type(keys=["id"], description="""Entity representing presence type""")
class PresenceTypeGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePresenceTypeByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Presence type name""")
    def name(self) -> str:
        return self.name
"""
from gql_empty.GraphResolvers import resolveTaskByID
@strawberryA.federation.type(keys=["id"], description=)
class TaskGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveTaskByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result
    
    @strawberryA.field(description=)
    def id(self, info: strawberryA.types.Info) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description=)
    def brief_des(self) -> str:
        return self.brief_des
"""

from gql_empty.GraphResolvers import resolvePresenceByID
@strawberryA.federation.type(keys=["id"], description="""Entity representing presence""")
class PresenceGQLModel:

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolvePresenceByID(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition
        return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self)-> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""Date of the event""")
    def date(self) -> str:
        return self.date
        

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from gql_empty.GraphResolvers import resolvePresenceTypeAll, resolvePresenceTypeByID
from gql_empty.GraphResolvers import resolvePresenceByID, resolvePresenceAll
from gql_empty.GraphResolvers import resolveTaskByID
from gql_empty.GraphResolvers import resolveContentByID

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Returns a list of presence types (paged)""")
    async def presence_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[PresenceTypeGQLModel]:
        result = await resolvePresenceTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result
   
