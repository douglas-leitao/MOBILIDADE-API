from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.usuario import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.pessoa import Person, PessoaCPF
from resources.veiculo import Veiculo, Veiculos
from resources.ocorrencia import Ocorrencia, Ocorrencias

from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@app.route('/')
def index():
    return "<h1>Deploy no heroku com sucesso!</h1>"

@jwt.token_in_blocklist_loader
def verifica_blacklist(self,token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': '/Você foi deslogado.'}), 401


api.add_resource(Person, '/pessoas/<string:person_id>')
api.add_resource(PessoaCPF, '/pessoa')
api.add_resource(Ocorrencia, '/ocorrencia/<string:ocorrencia_id>')
api.add_resource(Ocorrencias, '/ocorrencias')
api.add_resource(Veiculo, '/veiculo/<string:veiculo_id>')
api.add_resource(Veiculos, '/veiculos')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserConfirm, '/confirmacao/<int:user_id>')
#api.add_resource(Ocorrencia, '/')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
