from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
import sqlalchemy, os

def session_background( action):
    engine = create_engine('sqlite:///app/database/keys.db', echo=True, connect_args={'timeout': 100})
    Session = sessionmaker(bind=engine, autoflush=False) # ORM’s “handle” to the database is the Session:
    Session.configure(bind=engine)
    session = Session()
    metadata = Base.metadata

    def create():
        metadata.create_all(engine)
        session.commit()

    def delete():
        metadata.drop_all(bind = engine)

    def givesession():
        pass

    execute = {'create': create, 'delete': delete, 'session': givesession}
    execute.get(action)()
    return session
