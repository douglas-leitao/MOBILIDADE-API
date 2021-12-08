import traceback

from flask_restful import Resource, reqparse
from models.ocorrencia_veiculo import OcorrenciaVeiculoModel
from flask_jwt_extended import jwt_required

class OcorrenciaVeiculos(Resource):
    def get(self):
        return {'ocorrencia_veiculos': [veiculo.json() for veiculo in OcorrenciaVeiculoModel.query.all()]}

class Veiculo(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('placa')
    argumentos.add_argument('renavan')
    argumentos.add_argument('marca')

    def get(self, ocorrencia_id):
        veiculo = OcorrenciaVeiculoModel.find_veiculos_ocorrencia(ocorrencia_id)
        if veiculo:
            return veiculo.json(), 200
        return {'message': 'veiculo não encontrado'}, 404

    @jwt_required()
    def post(self, ocorrencia_id, renavan):
        print(ocorrencia_id)
        if OcorrenciaVeiculoModel.find_veiculos_ocorrencia(ocorrencia_id, renavan):
            return {"message": "Ocorrência ID '{}' já existe.".format(ocorrencia_id)}, 400 #BAD REQUEST
        dados = Veiculo.argumentos.parse_args()
        ocorrencia = OcorrenciaVeiculoModel(ocorrencia_id, **dados )
        try:
            ocorrencia.save_ocorrencia_veiculo()
        except:
            traceback.print_exc()
            return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'},  500
        return ocorrencia.json(), 200

    @jwt_required()
    def put(self, ocorrencia_id):
        dados = Veiculo.argumentos.parse_args()
        print("bug")
        veiculo_encontrado = OcorrenciaVeiculoModel.find_veiculos_ocorrencia(ocorrencia_id)
        if veiculo_encontrado:
            veiculo_encontrado.update_veiculo(**dados)
            try:
                veiculo_encontrado.save_veiculo()
            except:
                return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'}, 500
            return veiculo_encontrado.json(), 200
        veiculo = OcorrenciaVeiculoModel(ocorrencia_id, **dados)
        try:
            veiculo.save_ocorrencia_veiculo()
        except:
            return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'},  500
        return veiculo.json(), 201

    @jwt_required()
    def delete(self, ocorrencia_id):
        veiculo = OcorrenciaVeiculoModel.find_veiculos_ocorrencia(ocorrencia_id)
        if veiculo:
           try:
               veiculo.delete_veiculo()
           except:
               return {'message': 'Ocorreu um erro interno tentando salvar o veiculo.'}, 500
           return {'message': 'veiculo deletado'}, 200
        return {'message': 'veiculo não encontrado'}, 404
