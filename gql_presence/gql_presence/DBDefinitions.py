from sqlite3 import Date
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################


class PresenceModel(BaseModel):

    """Spravuje data spojené s účasti na události"""
    __tablename__ = 'presence'

    id = UUIDColumn()
    date = Column(DateTime)

    presenceType_id = Column(ForeignKey('presencetypes.id'),primary_key = True)
    presenceType = relationship('PresenceTypeModel', back_populates='presences')

    #definovat foreign key user_id
    user_id = Column(ForeignKey('user.id'),primary_key = True)
    users = relationship('UserModel', back_populates='presences')

    event_id = Column(ForeignKey('event.id'),primary_key = True)
    events = relationship('EventModel', back_populates='presences')

    taskOnEvent_id = Column(ForeignKey('taskonevent.id'),primary_key = True)
    taskOnEvents = relationship('TaskOnEventModel', back_populates='presences')


class PresenceTypeModel(BaseModel):
    """"
    Urcuje typ pritomnosti
    """
    __tablename__='presencetypes'

    id = UUIDColumn()
    name = Column(String)

    presences = relationship('PresenceModel', back_populates='presenceType')


class UserModel(BaseModel):

    """
    Spravuje usera
    """

    __tablename__='users'

    id = UUIDColumn()

    presences = relationship('PresenceModel', back_populates='users')
    

    

class EventModel(BaseModel):
    """
    Spravuje events
    """
    #tablename v množném čísle
    __tablename__='event'

    id = UUIDColumn()

    presences = relationship('PresenceModel', back_populates='events')

    

class TaskOnEventModel(BaseModel):

    __tablename__='taskonevent'

    id = UUIDColumn()
    name = Column(String)


    presences = relationship('PresenceModel', back_populates='taskOnEvents')
    task_id = Column(ForeignKey('task.id'),primary_key = True)
    tasks = relationship('TaskModel', back_populates='tasksOnEvents')
    
class TaskModel(BaseModel):

    __tablename__='task'

    id = UUIDColumn()
    brief_desc = Column(String)
    detail_desc = Column(String)
    reference = Column(String)
    date_of_entry = Column(DateTime)
    date_of_submission = Column(DateTime)
    date_of_fullfilment = Column(DateTime)

    tasksOnEvents = relationship('TaskOnEventModel', back_populates='tasks')

    

    content_id = Column(ForeignKey('content.id'),primary_key = True)
    contents = relationship('ContentModel', back_populates='tasks')


class ContentModel(BaseModel):

    __tablename__='content'

    id = UUIDColumn()
    brief_des = Column(String)
    detail_des = Column(String)

    tasks = relationship('TaskModel', back_populates='contents')
    





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring