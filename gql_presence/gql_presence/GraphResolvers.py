
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_presence.DBDefinitions import BaseModel, PresenceModel, PresenceTypeModel, UserModel, TaskOnEventModel

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# presence
resolvePresenceModelPage = createEntityGetter(PresenceModel)
resolvePresenceModelById = createEntityByIdGetter(PresenceModel)
# presence type

resolvePresenceTypeModelPage = createEntityGetter(PresenceTypeModel)
resolvePresenceTypeModelById = createEntityByIdGetter(PresenceTypeModel)

# user

resolveUserModelPage = createEntityGetter(UserModel)
resolveUserModelById = createEntityByIdGetter(UserModel)

# task on event

resolveTaskOnEventModelPage = createEntityGetter(TaskOnEventModel)
resolveTaskOnEventModelById = createEntityByIdGetter(TaskOnEventModel)

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