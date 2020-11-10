from collections import OrderedDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()
class UserDto(Base):
    # def __init__(self, id, name, password):
    #     self.id = id
    #     self.name = name
    #     self.password = password

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(12))
    password = Column(String(12))
    def __repr__(self):
        return OrderedDict(id=self.id,
                           name=self.name,
                           password=self.password)
