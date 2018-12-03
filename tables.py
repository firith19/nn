from sqlalchemy import Column, ForeignKey, create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, validates
from sqlalchemy import Integer, String, Unicode, DateTime, Date, SmallInteger, BLOB, Time, Text, Boolean
from sqlalchemy.dialects.mysql import MEDIUMTEXT, TINYINT, BIT, FLOAT
from sqlalchemy.sql import select

Base = declarative_base()
db_uri_dictionary = {}

def get_class_by_table_name(table_name):
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
            return c

def init_db(db_uri='mysql+mysqlconnector://ematdin:KrejVaf2!@localhost/nn?auth_plugin=mysql_native_password'):
    global engine
    global session
    global db_uri_dictionary
    if db_uri not in db_uri_dictionary:
        engine = create_engine(db_uri)
        session = Session(bind=engine)
        db_uri_dictionary[db_uri] = session
        return session
    return db_uri_dictionary[db_uri]

def does_dokument_exist(dict):
    global session
    if session:
        rows = session.query(Dokument).filter_by(**dict)
        if rows.count() >= 1:
            return True
    return False

class Dokument_download(Base):
    __tablename__ = 'dokument_download'
    nn_id = Column(Integer, primary_key=True, nullable=False)
    ime_dokumenta = Column(String(200))

    def __repr__(self):
        return "<Dokument_download: nn_id=%s, ime_dokumenta=%s>" % (
            str(self.nn_id), self.ime_dokumenta)

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Dokument_download, self).__init__(**kwargs)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    msg = Column(String(200))
    log_level = Column(String(8))

    def __repr__(self):
        return "<Log: id=%s, msg=%s, level=%s>" % (
            str(self.id), self.msg, self.log_level)

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Log, self).__init__(**kwargs)

class Dokument(Base):
    __tablename__ = 'dokument'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nn_id = Column(Integer)
    oznaka_broj = Column(String(32))
    naziv = Column(String(200))
    vrsta_dokumenta = Column(String(200))
    vrsta_ugovora = Column(String(200))
    cpv = Column(String(200))
    vrsta_postupka = Column(String(200))
    rok_za_dostavu_ponuda = Column(DateTime, nullable=False)
    datum_objave = Column(DateTime, nullable=False)
    datum_slanja = Column(DateTime, nullable=False)
    zakon = Column(String(200))
    ime_dokumenta = Column(String(200))

    def __repr__(self):
        return "<Dokument: id=%s, nn_id=%s, oznaka_broj=%s, naziv=%s>" % (
            str(self.id), str(self.nn_id), self.oznaka_broj, self.naziv)

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Dokument, self).__init__(**kwargs)

class Firma(Base):
    __tablename__ = 'firma'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    oib = Column(String(16))

    def __repr__(self):
        return "<Firma: id=%s, oib=%s>" % (
            str(self.id), self.oib)

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Firma, self).__init__(**kwargs)

class Ponuda(Base):
    __tablename__ = 'ponuda'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firma_id = Column(Integer)
    iznos = Column(FLOAT)
    dobila = Column(Boolean)

    def __repr__(self):
        return "<Ponuda: id=%s, firma_id=%s, iznos=%s, dobila=%s>" % (
            str(self.id), str(self.firma_id), self.iznos, str(self.dobila))

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Ponuda, self).__init__(**kwargs)


class Dokument_ponuda(Base):
    __tablename__ = 'dokument_ponuda'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dokument_id = Column(Integer, ForeignKey('dokument.id'))
    ponuda_id = Column(Integer, ForeignKey('ponuda.id'))

    def __repr__(self):
        return "<Dokument_ponuda: id=%s, dokument_id=%s, ponuda_id=%s>" % (
            str(self.id), str(self.dokument_id), str(self.ponuda_id))

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Dokument_ponuda, self).__init__(**kwargs)

class Dokument_firma(Base):
    __tablename__ = 'dokument_firma'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dokument_id = Column(Integer, ForeignKey('dokument.id'))
    firma_id = Column(Integer, ForeignKey('firma.id'))

    def __repr__(self):
        return "<Dokument_ponuda: id=%s, dokument_id=%s, firma_id=%s>" % (
            str(self.id), str(self.dokument_id), str(self.firma_id))

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Dokument_firma, self).__init__(**kwargs)

class Dokument_dokument(Base):
    __tablename__ = 'dokument_dokument'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dokument1_id = Column(Integer, ForeignKey('dokument.id'))
    dokument2_id = Column(Integer, ForeignKey('dokument.id'))

    def __repr__(self):
        return "<Dokument_ponuda: id=%s, dokument1_id=%s, dokument2_id=%s>" % (
            str(self.id), str(self.dokument1_id), str(self.dokument2_id))

    def __init__(self, **kwargs):
        # global session
        # nick_name = kwargs['NickName']
        # res = session.query(Person).filter_by(NickName=nick_name).one()
        # if not res:
        super(Dokument_dokument, self).__init__(**kwargs)

