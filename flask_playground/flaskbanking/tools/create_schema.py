from db.dbinit import DB_GLOBALBANK, get_engine, DB_PIGGYBANK
from model.globalbank.base import GlobalBankBase
from model.piggybank.base import PiggyBankBase

def main():
    # Imports Required for metadata init
    from model.globalbank.member import MemberBalance
    GlobalBankBase.metadata.create_all(get_engine(DB_GLOBALBANK))
    from model.piggybank.tummy import  TummyBalance
    PiggyBankBase.metadata.create_all(get_engine(DB_PIGGYBANK))

    
if __name__ == '__main__':
    main()
    