from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from model.piggybank.base import PiggyBankBase

class TummyBalance(PiggyBankBase):
    __tablename__ = 'tummy_balance'

    id = Column(Integer, primary_key=True)
    member_name = Column(String)
    which_piggy = Column(String) # like an account
    balance = Column(Integer)

    def __init__(self, member_name, which_piggy, balance):
        self.member_name = member_name
        self.which_piggy = which_piggy
        self.balance = balance

    def __repr__(self):
       return 'TummyBalance( {}, {}, {} )'.format(self.member_name, self.which_piggy, self.balance)

  