from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Check all needed components of the database and create the needed ones if didn't exist


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    email = Column(String)
    password = Column(String)
    nfc_id = Column(Integer)
    user_flow = Column(Integer)

    def __repr__(self):
        return "<User(username='%s', fullname='%s', email='%s', password='%s', nfc_id='%i', user_flow='%s')>" % (
            self.username, self.fullname, self.email, self.password, self.nfc_id, self.user_flow)


class Keg(Base):
    __tablename__ = 'keg'
    id = Column(Integer, primary_key=True)
    keg_id = Column(Integer)
    keg_flow = Column(Integer)

    def __repr__(self):
        return "<User(keg_id='%i', keg_flow='%i')>" % (self.keg_id, self.keg_flow)


path_to_db = 'database_task3.db'
engine = create_engine('sqlite:///' + path_to_db)
Base.metadata.create_all(engine)