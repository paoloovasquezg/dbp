#imports
import sys
from crypt import methods
from flask import (
    Flask,
    abort,
    jsonify, 
    render_template, 
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#models
class Person(db.Model):
    __tablename__ = 'personas'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    apellidos = db.Column(db.String(), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    residencia = db.Column(db.String(), nullable=False)


    def __repr__(self):
        return f'Todo: id={self.id}, nombre={self.nombre}, apellidos={self.apellidos}, edad={self.edad}, residencia={self.residencia} '

#db.create_all()

#controller
@app.route('/', methods=['GET'])
def index():
    return render_template('index3.html', data=Person.query.all())


@app.route('/personas/ingreso_normal', methods=['POST'])
def create_todo_get():
    try:
        nombre = request.form.get('nombre', '')
        apellidos = request.form.get('apellidos', '')
        edad = request.form.get('edad', '')
        residencia = request.form.get('residencia', '') 
        person = Person(nombre=nombre,apellidos=apellidos,edad=edad,residencia=residencia)
        db.session.add(person)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


#run
if __name__ == '__main__':
    app.run(debug=True, port=5001)