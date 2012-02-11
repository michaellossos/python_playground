from sqlalchemy import Column, Integer, String
from model.globalbank.base import GlobalBankBase

class MemberBalance(GlobalBankBase):
    __tablename__ = 'member_balance'

    id = Column(Integer, primary_key=True)
    member_name = Column(String)
    account = Column(String)
    balance = Column(Integer)

    def __init__(self, member_name, account, balance):
        self.member_name = member_name
        self.account = account
        self.balance = balance

    def __repr__(self):
       return 'MemberBalance( {}, {}, {} )'.format(self.member_name, self.account, self.balance)
