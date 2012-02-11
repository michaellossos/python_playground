import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

def _create_sqlite_engine(db_file):
    if not db_file:
        raise ValueError('Parameter db_file must be specified.')
    # TODO Get from env
    data_dir = os.path.abspath('{}/../../../data/'.format(__file__))
    if not os.path.exists(data_dir):
        # TODO logging
        print 'Making dir: {}'.format(data_dir)
        os.mkdir(data_dir)

    sqlite_db_file = '{}/{}'.format(data_dir, db_file)
    engine = create_engine('sqlite:///{}'.format(sqlite_db_file), echo=True)
    engine.execute("select 1").scalar()
    return engine

def get_engine(db_name):
    if not db_name:
        raise ValueError('Parameter db_name must be specified.')
    return _create_sqlite_engine('{}.sqlite'.format(db_name))

def get_session_for_engine(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def get_session(db_name):
    return get_session_for_engine(get_engine(db_name))

DB_GLOBALBANK = 'globalbank'
DB_PIGGYBANK = 'piggybank'

