
from collections import OrderedDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()
class StockAhNameDict(Base):
    __tablename__ = 'stock_zh_ah_name_dict'
    code = Column(String(32), primary_key=True)
    name = Column(String(64))
