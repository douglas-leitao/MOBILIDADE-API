from flask_restful import Resource, reqparse
from models.pessoa import PersonModel
from flask_jwt_extended import jwt_required

argumentos = reqparse.RequestParser()
argumentos.add_argument('cpf')
argumentos.add_argument('rg')
argumentos.add_argument('uf_rg')
argumentos.add_argument('nome')
argumentos.add_argument('data_nasc')
argumentos.add_argument('sexo')
#
argumentos.add_argument('n_registro')
argumentos.add_argument('uf_reg')
argumentos.add_argument('cat_hab')
argumentos.add_argument('validade')
argumentos.add_argument('primeira_hab')
#
argumentos.add_argument('telefone')
argumentos.add_argument('email')
argumentos.add_argument('logradouro')
argumentos.add_argument('log_nro')
argumentos.add_argument('complemento')
argumentos.add_argument('bairro')
argumentos.add_argument('cidade')
argumentos.add_argument('uf')


class Persons(Resource):
    def get(self):
        return {'pessoas': [pessoa.json() for pessoa in PersonModel.query.all()]}


class Person(Resource):

    def get(self, person_id):
        person = PersonModel.find_person(person_id)
        if person:
            return person.json(), 200
        return {'message': 'pessoa não encontrada'}, 404

    @jwt_required()
    def post(self, person_id):
        if PersonModel.find_person(person_id):
            return {"message": "Person ID '{}' não existe.".format(person_id)}, 400  # BAD REQUEST
        dados = Person.argumentos.parse_args()
        person = PersonModel(person_id, **dados)
        try:
            person.save_person()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
        return person.json(), 200

    @jwt_required()
    def put(self, person_id):
        dados = Person.argumentos.parse_args()
        person_encontrado = PersonModel.find_person(person_id)
        if person_encontrado:
            person_encontrado.update_person(**dados)
            try:
                person_encontrado.save_person()
            except:
                return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
            return person_encontrado.json(), 200
        person = PersonModel(person_id, **dados)
        try:
            person.save_person()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
        return person.json(), 201

    @jwt_required()
    def delete(self, person_id):
        pessoa = PersonModel.find_person(person_id)

        if pessoa:
            try:
                pessoa.delete_person()
            except:
                return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
            return {'message': 'Pessoa deletada'}, 200
        return {'message': 'Pessoa não encontrada'}, 404


class PessoaCPF(Resource):
    @jwt_required()
    def patch(self):
        dados = argumentos.parse_args()
        teste = dados['cpf']
        print(teste)

        pessoa_encontrada = PersonModel.find_by_cpf(dados['cpf'])

        if pessoa_encontrada:
            pessoa_encontrada.update_person(**dados)
            try:
                pessoa_encontrada.save_person()
            except:
                return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
            return pessoa_encontrada.json(), 200
        person = PersonModel(dados['cpf'], **dados)
        try:
            person.save_person()
        except:
            return {'message': 'Ocorreu um erro interno ao tentar salvar a pessoa.'}, 500
        return person.json(), 201
