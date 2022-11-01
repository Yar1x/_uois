
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_empty.DBDefinitions import BaseModel, PresenceModel, PresenceTypeModel, TaskModel, ContentModel

#presence resolvers
resolvePresenceByID = createEntityByIdGetter(PresenceModel)
resolveTypeForPresence = create1NGetter(PresenceTypeModel, foreignKeyName = 'presence_id', options=joinedload(PresenceTypeModel.presence))
resolveTaskForPresence = create1NGetter(TaskModel,foreignKeyName='presence_id',options=joinedload(TaskModel.presence))

#presenceType resolvers

resolvePresenceTypeByID = createEntityByIdGetter(PresenceTypeModel)
resolvePresenceTypeAll = createEntityGetter(PresenceTypeModel)

async def resolvePresenceByPresenceType(session,presencetypeId):
    stmt = select(PresenceModel).join(PresenceTypeModel).where(PresenceModel.presenceType_id == presencetypeId)
    dbSet = await session.execute(stmt)
    result = dbSet.scalars()
    return result

#task resolvers

resolveTaskByID = createEntityByIdGetter(TaskModel)

#content resolver

resolveContentByID = createEntityByIdGetter(ContentModel)
## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################



###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################


# ...