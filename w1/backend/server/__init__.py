import json
from flask import (
    Flask,
    abort,
    jsonify,
    request
)

from flask_cors import CORS, cross_origin

from models import setup_db, Usuario, Radio, RadioUsuario

TODOS_PER_PAGE=5
    

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # , origins = ['https://utec.edu.pe', 'http://127.0.0.1:5001'], max_age = 10)

    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        selection = Usuario.query.order_by('id').all()
        usuarios = [usuario.format() for usuario in selection]

        if len(usuarios) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'usuarios': usuarios,
            'total_usuarios': len(selection)
        })

    @app.route('/radios', methods = ['GET'])
    def get_radios():
        selection = Radio.query.order_by('id').all()
        radios = [radio.format() for radio in selection]

        if len(radios) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'radios': radios,
            'total_radios': len(selection)
        })

    @app.route('/radiosusuarios', methods = ['GET'])
    def get_radiousuarios():
        selection = RadioUsuario.query.order_by('usuario').all()
        radiousuarios = [radiousuarios.format() for radiousuarios in selection]

        if len(radiousuarios) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'radiosusuarios': radiousuarios,
            'total_radiosusuarios': len(selection)
        })

    @app.route('/usuarios', methods = ['POST'])
    def insert_usuario():
        body = request.get_json()

        name = body.get('name', None)

        if name is None:
            abort(422)

        usuario = Usuario(name=name)
        new_usuario_id = usuario.insert()

        selection = Usuario.query.order_by('id').all()
        usuarios = [usuario.format() for usuario in selection]

        return jsonify({
            'success': True,
            'created': new_usuario_id,
            'usuarios': usuarios,
            'total_usuarios': len(selection)
        })

    @app.route('/radios', methods=['POST'])
    def insert_radio():
        body = request.get_json()

        name = body.get('name', None)

        if name is None:
            abort(422)

        radio = Radio(name=name)
        new_radio_id = radio.insert()

        selection = Radio.query.order_by('id').all()
        radios = [radio.format() for radio in selection]

        return jsonify({
            'success': True,
            'created': new_radio_id,
            'radios': radios,
            'total_radios': len(selection)
        })

    @app.route('/radiosusuarios', methods=['POST'])
    def insert_radiousuario():
        body = request.get_json()
        name = body.get('name', None)

        if name is None:
            abort(422)

        radio = Radio(name=name)
        new_radio_id=radio.insert()

        usuario = Usuario(name=name)
        new_usuario_id=usuario.insert()

        radiousuario = RadioUsuario(usuario=new_usuario_id, radio=new_radio_id)
        radiousuario.insert()

        selection = RadioUsuario.query.order_by('usuario').all()
        radiousuarios = [radiousuarios.format() for radiousuarios in selection]

        return jsonify({
            'success': True,
            'radiosusuarios': radiousuarios,
            'total_radiosusuarios': len(selection)
        })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    return app
