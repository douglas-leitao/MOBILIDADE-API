import traceback

from flask_restful import Resource, reqparse
from models.veiculo import VeiculoModel
from flask_jwt_extended import jwt_required

class Veiculos(Resource):
    def get(self):
        return {'veiculos': [veiculo.json() for veiculo in VeiculoModel.query.all()]}

class Veiculo(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('placa')
    argumentos.add_argument('renavan')
    argumentos.add_argument('marca')
    argumentos.add_argument('modelo')
    argumentos.add_argument('ano_modelo')
    argumentos.add_argument('cor')
    argumentos.add_argument('especie')
    argumentos.add_argument('tipo')
    argumentos.add_argument('categoria')
    argumentos.add_argument('proprietario_fk')

    def get(self, veiculo_id):
        veiculo = VeiculoModel.find_veiculo(veiculo_id)
        if veiculo:
            return veiculo.json(), 200
        return {'message': 'veiculo não encontrado'}, 404

    @jwt_required()
    def post(self, veiculo_id):
        print(veiculo_id)
        if VeiculoModel.find_veiculo(veiculo_id):
            return {"message": "Veiculo ID '{}' já existe.".format(veiculo_id)}, 400 #BAD REQUEST
        dados = Veiculo.argumentos.parse_args()
        veiculo = VeiculoModel(veiculo_id, **dados )
        try:
            veiculo.save_veiculo()
        except:
            traceback.print_exc()
            return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'},  500
        return veiculo.json(), 200

    @jwt_required()
    def put(self, veiculo_id):
        dados = Veiculo.argumentos.parse_args()
        print("bug")
        veiculo_encontrado = VeiculoModel.find_veiculo(veiculo_id)
        if veiculo_encontrado:
            veiculo_encontrado.update_veiculo(**dados)
            try:
                veiculo_encontrado.save_veiculo()
            except:
                return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'}, 500
            return veiculo_encontrado.json(), 200
        veiculo = VeiculoModel(veiculo_id, **dados)
        try:
            veiculo.save_veiculo()
        except:
            return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'},  500
        return veiculo.json(), 201

    @jwt_required()
    def delete(self, veiculo_id):
        veiculo = VeiculoModel.find_veiculo(veiculo_id)
        if veiculo:
           try:
               veiculo.delete_veiculo()
           except:
               return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'}, 500
           return {'message': 'veiculo deletado'}, 200
        return {'message': 'veiculo não encontrado'}, 404
