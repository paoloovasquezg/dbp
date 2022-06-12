#Importes
from flask import Flask, request, render_template #render --> para redireccionar al html
from flask_sqlalchemy import SQLAlchemy

#Configuracion - Instancia
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/dbp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelos
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable = False)

    def __repr__(self):
        return 'Person: id={}, name={}'.format(self.id, self.name)

db.create_all()

#ruta basica
@app.route('/')
#el get
def index():
    #devolver instancia de tabla
    #persons = Person.query.all()[1] #Para cierto elemento
    persons = Person.query.all() #Para todos elementos
    return 'Hello {}'.format((", ".join([p.name for p in persons])))

#Nueva ruta: URL Query Parameters
@app.route('/greetings')
def greetings():
    name = request.args.get('name','')
    lastname = request.args.get('lastname','')
    greetings_str = 'Hello {} {}'.format(name,lastname)
    #envio informacion al html -- redireccionar a este
    return render_template('index.html',data=greetings_str)


#ejecutar aplicacion
#por terminal - nombre archivo; debug: tome en cuenta los cambios
if __name__ == '__main__':
    app.run(debug=True)
else: #por comandos - flask run
    print("running the app by commands")