from  sqlalchemy import TIMESTAMP, BigInteger, CheckConstraint, Column,Integer,String,Boolean,DateTime, text
from database import Base
from datetime import datetime
class Voter(Base):
    __tablename__="vote"


    voter_id=Column(BigInteger,primary_key=True,nullable=False)
    name=Column(String, unique=True, nullable=False)
    password=Column(String,nullable=False)
    status=Column(Boolean,default=False)
    time = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    voted_party = Column(String,nullable=True)

    __table_args__ = (
        CheckConstraint('voted_party IS NOT NULL OR status = false', name='valid_voting_constraint'),
    )