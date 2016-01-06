from app.extensions import cache, bcrypt
from app.database import db, CRUDMixin
import datetime

class Promena(CRUDMixin, db.Model):
    __tablename__ = 'promena'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    promena = db.Column(db.String(100), nullable=True)
    hodnota = db.Column(db.String(10))
    def __init__(self, promena, hodnota):
        self.promena = promena
        self.hodnota = hodnota
    @staticmethod
    def vypis(id):
        return db.session.query(Promena.hodnota).filter_by(promena = id).first_or_404()

    @staticmethod
    def hodnota_uloz(nazev,value):
        id=Promena.query.filter_by(promena = id).first_or_404()
        if id:
            id.hodnota = str(value)
            id.update()
        else:
            id = Promena.create(
                promena = nazev,
                hodnota = str(value))
        return True
    @classmethod
    def stats(cls):
        return {
            'all': 'xxx',
            'active': 'xxx',
            'inactive': 'xxx'
        }


class Product(CRUDMixin, db.Model):
    __tablename__ = 'product'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    UID = db.Column(db.String(10), nullable=False,index=True)
    Obj = db.Column(db.String(10), nullable=False, unique=True)
    Popis = db.Column(db.String(120), nullable=False)
    Skupina = db.Column(db.String(10), nullable=False)
    CenaProdej = db.Column(db.Float)
    sklad=db.Column(db.String(10))
    MJ = db.Column(db.String(5))
    KL = db.Column(db.String(100), nullable=True)
    TL = db.Column(db.String(100), nullable=True)
    Foto = db.Column(db.String(100), nullable=True)
    Poznamka = db.Column(db.String(150), nullable=True)
    date_update=db.Column(db.DateTime)

    def __init__(self, **kwargs):
        #self.datum_insertu = datetime.utcnow()
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
    @staticmethod
    def find_by_UID(id):
        return db.session.query(Product).filter_by(UID = id).first()
    @staticmethod
    def find_by_id(id):
        return db.session.query(Product).filter_by(id = id).first()
    @staticmethod
    def find_by_Obj(id):
        return db.session.query(Product).filter_by(Obj = id).first()
    @staticmethod
    def filter_by_Popis(text):
        return Product.query.filter(Product.Popis.contains(text)).all()

    @staticmethod
    def all():
        return db.session.query(Product).all()
    @staticmethod
    def notKL():
        return db.session.query(Product).filter_by(KL = None).all()

    @classmethod
    def stats(cls):
        return {
            'all': 'xxx',
            'active': 'xxx',
            'inactive': 'xxx'
        }



#    def __init__(self):
