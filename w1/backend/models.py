from collections import UserString
from tkinter import CASCADE
from flask_sqlalchemy import SQLAlchemy

database_name='practica'
database_path='postgresql://{}:{}@{}/{}'.format('postgres','1234','localhost:5432', database_name)
#'postgresql://postgres@localhost:5432/todoapp10'
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI']=database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    radios = db.relationship('Radio', secondary='radiousuarios', lazy = True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Radio(db.Model):
    __tablename__ = 'radios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    usuarios = db.relationship('Usuario', secondary='radiousuarios', lazy=True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            "id": self.id,
            "name": self.name
        }


class RadioUsuario(db.Model):
    __tablename__ = 'radiousuarios'
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete=CASCADE, onupdate=CASCADE),primary_key=True)
    radio = db.Column(db.Integer, db.ForeignKey('radios.id', ondelete=CASCADE, onupdate=CASCADE), primary_key=True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            "user_id": self.usuario,
            "radio_id": self.radio
        }
