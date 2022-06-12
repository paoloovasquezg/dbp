#imports
from email.policy import default
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/todoapp10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#models
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'Todo: id={self.id}, description={self.description}'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'TodoList: id={self.id}, description={self.name}'


#db.create_all()

#controller
@app.route('/todos/<todo_id>/delete-todo', methods=['DELETE'])
def delete_todo(todo_id):
    response = {}
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        response['success'] = True
    except:
        response['success'] = False
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(response)

@app.route('/lists/<list_id>')
def get_lists_todos(list_id):
    return render_template('index.html',
    lists=TodoList.query.all(),
    current_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    )

@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('get_lists_todos', list_id=1))



@app.route('/lists/create', methods=['POST'])
def create_list():
    response = {}
    try:
        name = request.get_json()['name']
        list = TodoList(name=name)
        db.session.add(list)
        db.session.commit()
        response['id'] = list.id
        response['name'] = name
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(response)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    response = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description)
        todo.list_id = list_id
        db.session.add(todo)
        db.session.commit()
        response['id'] = todo.id
        response['description'] = description
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(response)

@app.route('/todos/create_get', methods=['GET'])
def create_todo_get():
    try:
        description = request.args.get('description', '')
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def update_completed(todo_id):
    try:
        new_completed = request.get_json()['new_completed']
        todo = Todo.query.get(todo_id)
        todo.completed = new_completed
        db.session.commit()
        return redirect(url_for('index'))
    except:
        db.session.rollback()
    finally:
        db.session.close()
    

#run
if __name__ == '__main__':
    app.run(debug=True, port=5001)

