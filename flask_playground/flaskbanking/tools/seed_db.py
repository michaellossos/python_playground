from db.dbinit import DB_GLOBALBANK, get_session, DB_PIGGYBANK, get_engine
from model.globalbank.member import MemberBalance
from model.piggybank.tummy import TummyBalance

def _seed(members, db_name):
    session = get_session(db_name)
    for m in members:
        session.add(m)

    session.commit()

def seed_globalbank():
    members = [
        MemberBalance('John Smith', '123456789', 888),
        MemberBalance('Jane Archer', '987623111', 3000)
    ]
    _seed(members, DB_GLOBALBANK)


def seed_piggybank():
    members = [
        TummyBalance('Little Timmy', 'Pink Piggy', 3),
        TummyBalance('Little Sally', 'Purple Piggy', 8)
    ]
    _seed(members, DB_PIGGYBANK)

def _query(db_name, model_class):
    session_new = get_session(db_name)
    print '____________ {} ___________ '.format(db_name)
    print session_new.query(model_class).all()

def query_banks():
    _query(DB_GLOBALBANK, MemberBalance)
    _query(DB_PIGGYBANK, TummyBalance)

def main():
    seed_globalbank()
    seed_piggybank()
    query_banks()

if __name__ == '__main__':
    main()

  