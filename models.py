from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///phones.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname= Column(String)
    birthday = Column(String)
    nickname = Column(String)
    phones = relationship("Phone", back_populates="user")
    def __str__(self):
        return self.birthday
    
    @classmethod
    def add(cls, name, surname,nickname, birthday):
        user = cls(name=name,surname=surname,nickname=nickname, birthday=birthday)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def all(cls): 
        return session.query(cls).all()

    @classmethod
    def search_by_name(cls, name, surname):
        user = session.query(cls).filter(User.name == name, User.surname == surname).first()
        return user
    @classmethod
    def search_by_ID(cls, user_id):
        user = session.query(cls).filter(User.id == user_id).first()
        return user

    @classmethod
    def delete(cls,name,surname):
        delete_user = session.query(User).filter(User.name == name, User.surname == surname).first()
        session.delete(delete_user)
        session.commit()



class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="phones")

    def __str__(self):
        return self.phone

    @classmethod
    def all(cls):
        return session.query(cls).all()
    @classmethod
    def add(cls, phone, user):
        phone = cls(phone=phone, user=user)
        session.add(phone)
        session.commit()
        return phone


Base.metadata.create_all(engine)