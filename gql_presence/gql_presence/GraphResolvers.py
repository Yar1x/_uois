
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_presence.DBDefinitions import BaseModel, PresenceModel, PresenceTypeModel, UserModel, TaskOnEventModel, TaskModel, ContentModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# presence
resolvePresenceModelPage = createEntityGetter(PresenceModel)
resolvePresenceModelById = createEntityByIdGetter(PresenceModel)
#přejmenovat
resolvePresenceForUser = create1NGetter(PresenceModel,foreignKeyName='user_id') 

# presence type

resolvePresenceTypeModelPage = createEntityGetter(PresenceTypeModel)
resolvePresenceTypeModelById = createEntityByIdGetter(PresenceTypeModel)

# user

resolveUserModelPage = createEntityGetter(UserModel)
resolveUserModelById = createEntityByIdGetter(UserModel)

# task on event

resolveTaskOnEventModelPage = createEntityGetter(TaskOnEventModel)
resolveTaskOnEventModelById = createEntityByIdGetter(TaskOnEventModel)

# tasks

resolveTaskModelByPage = createEntityGetter(TaskModel)
resolveTaskModelById = createEntityByIdGetter(TaskModel)

# content

resolveContentModelByPage = createEntityGetter(ContentModel)
resolveContentModelById = createEntityByIdGetter(ContentModel)


###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

# resolveItemById = createEntityByIdGetter(EntityModel)
# resolveItemPage = createEntityGetter(EntityModel)

# ...