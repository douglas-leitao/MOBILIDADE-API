#import flask_jwt_extended
from flask_jwt_extended import jwt_required, create_access_token, get_jwt

from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from models.usuario import UserModel
import traceback
from flask import make_response, render_template

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' não pode ser deixado em branco")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' não pode ser deixado em branco")
atributos.add_argument('ativado', type=bool)
atributos.add_argument('email',  type=str)

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json(), 200
        return {'message': 'usuário não encontrado'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
           try:
               user.delete_user()
           except:
               return {'message': 'Ocorreu um erro interno ao tentar deletar o usuário.'}, 500
           return {'message': 'Usuário deletado'}, 200
        return {'message': 'Usuário não encontrado'}, 404

class UserRegister(Resource):

    def post(self):
        dados = atributos.parse_args()

        if not dados.get('email') or dados.get('email') is None:
            return {"message": "O campo 'email' não pode ser deixado em branco"}, 400

        if UserModel.find_by_email(dados['email']):
            return {"message": "O e-mail '{}' já está em uso.".format(dados['email'])}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message": "O login '{}' já está em uso.".format(dados['login'])}, 400

        user = UserModel(**dados)
        user.ativado = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exec()
            return {'message' : 'Ocorreu um erro interno no server.'}, 500
        return {"message": "O login foi criado com sucesso"}, 201

class UserLogin(Resource):
    @classmethod
    def get(cls):
        return render_template('login.html')


    # AUTENTICA LOGIN
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
                return {'access_token': token_de_acesso}, 200
            return {"message": "Usuário não confirmado"}, 400
        return {"message": "O Usuário ou a Senha está incorreta"}, 401
        #return {"message": dados['login']}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Deslogado com sucesso!'}, 200

class UserConfirm(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "Usuário id '{}' não encontrado".format(user_id)}, 404

        user.ativado = True
        user.save_user()
        #return {"message": "Usuário id '{}' confirmado com sucesso!".format(user_id)}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200, headers)