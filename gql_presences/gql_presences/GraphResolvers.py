from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from gql_presences.DBDefinitions import (
    BaseModel,
    PresenceModel,
    PresenceTypeModel,
    TaskModel,
    ContentModel,
    EventModel,
)

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

# user
#resolveUserModelPage = createEntityGetter(UserModel)
#resolveUserModelById = createEntityByIdGetter(UserModel)

# PresenceModel
resolvePresenceModelPage = createEntityGetter(PresenceModel)
resolvePresenceModelById = createEntityByIdGetter(PresenceModel)

resolveAddPresense = createInsertResolver(PresenceModel)

# Presences for User
resolvePresencesForUser = create1NGetter(PresenceModel,foreignKeyName='user_id') 

# Presences for event
resolvePresencesOnEvent = create1NGetter(PresenceModel, foreignKeyName='event_id')


# PresenceTypeModel
resolvePresenceTypeModelPage = createEntityGetter(PresenceTypeModel)
resolvePresenceTypeModelById = createEntityByIdGetter(PresenceTypeModel)

# Presences for presence types
resolvePresencesForPresenceType = create1NGetter(PresenceModel, foreignKeyName='presenceType_id')


# task on event
resolveTasksForUser = create1NGetter(TaskModel, foreignKeyName="user_id")

# TaskModel
resolveTaskModelByPage = createEntityGetter(TaskModel)
resolveTaskModelById = createEntityByIdGetter(TaskModel)

# Tasks for Event
resolveTasksForEvent = create1NGetter(TaskModel, foreignKeyName="event_id")

# ContentModel
resolveContentModelByPage = createEntityGetter(ContentModel)
resolveContentModelById = createEntityByIdGetter(ContentModel)

# Content for Event
resolveContentForEvent = create1NGetter(ContentModel, foreignKeyName="event_id")

# Event

resolveUpdateEvent = createUpdateResolver(EventModel)

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
