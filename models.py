from  sqlalchemy import TIMESTAMP, BigInteger, Column,Integer,String,Boolean,DateTime, text
from database import Base
from datetime import datetime
class Voter(Base):
    __tablename__="vote"


    voter_id=Column(BigInteger,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    password=Column(String,nullable=False)
    status=Column(Boolean,default=True)
    time = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))