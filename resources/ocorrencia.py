import traceback
from datetime import date
from flask_restful import Resource, reqparse
from models.ocorrencia import OcorrenciaModel
from flask_jwt_extended import jwt_required
from flask import make_response, render_template


class Ocorrencias(Resource):

    def get(self):
        return {'ocorrencias': [ocorrencia.json() for ocorrencia in OcorrenciaModel.query.all()]}

class Ocorrencia(Resource):
    argumentos_bo = reqparse.RequestParser()
    argumentos_bo.add_argument('data_sinistro')
    argumentos_bo.add_argument('hora_sinistro')
    argumentos_bo.add_argument('cidade')
    argumentos_bo.add_argument('logradouro')
    argumentos_bo.add_argument('log_nro')
    argumentos_bo.add_argument('complemento')
    argumentos_bo.add_argument('bairro')
    argumentos_bo.add_argument('tipo_sinistro')
    argumentos_bo.add_argument('clima')
    argumentos_bo.add_argument('mao_direcao')
    argumentos_bo.add_argument('tipo_pavimento')
    argumentos_bo.add_argument('superficie_pista')
    argumentos_bo.add_argument('controle_trafego')
    argumentos_bo.add_argument('iluminacao')
    argumentos_bo.add_argument('velocidade_via')

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def get(self, ocorrencia_id):
        ocorrencia = OcorrenciaModel.find_ocorrencia(ocorrencia_id)
        if ocorrencia:
            return ocorrencia.json(), 200
        return {'message': 'Ocorrencia não encontrada'}, 404

    @jwt_required()
    def post(self, ocorrencia_id):

        data_bo = date.today()
        dia_bo = data_bo.day
        mes_bo = data_bo.month
        ano_bo = data_bo.year

        bo_id = str(ano_bo) + '' + str(mes_bo).zfill(2) +''+ str(dia_bo).zfill(2) +''+ ocorrencia_id.zfill(2)
        print(bo_id)

        if OcorrenciaModel.find_ocorrencia(bo_id):
            return {"message": "Ocorrencia ID '{}' já existe.".format(bo_id)}, 400 #BAD REQUEST

        dados = Ocorrencia.argumentos_bo.parse_args()
        ocorrencia = OcorrenciaModel(bo_id,**dados)
        try:
            ocorrencia.save_ocorrencia()
        except:
            traceback.print_exc()
            return {'message': 'Ocorreu um erro interno tentando salvar a oorrência.'},  500
        return ocorrencia.json(), 200

    @jwt_required()
    def put(self, ocorrencia_id):
        dados = Ocorrencia.argumentos_bo.parse_args()
        ocorrencia_encontrada = OcorrenciaModel.find_ocorrencia(ocorrencia_id)
        if ocorrencia_encontrada:
            ocorrencia_encontrada.update_ocorrencia(**dados)
            try:
                ocorrencia_encontrada.save_ocorrencia()
            except:
                return {'message': 'Ocorreu um erro interno tentando salvar a oorrência.'}, 500
            return ocorrencia_encontrada.json(), 200
        ocorrencia = OcorrenciaModel(ocorrencia_id, **dados)
        try:
            ocorrencia.save_ocorrencia()
        except:
            return {'message': 'Ocorreu um erro interno tentando salvar a oorrência.'},  500
        return ocorrencia.json(), 201


    @jwt_required()
    def delete(self, ocorrencia_id):
        ocorrencia = OcorrenciaModel.find_ocorrencia(ocorrencia_id)

        if ocorrencia:
           try:
               ocorrencia.delete_ocorrencia()
           except:
               traceback.print_exec()
               return {'message': 'Ocorreu um erro interno tentando deletar a oorrência.'}, 500
           return {'message': 'Ocorrencia deletada'}, 200
        return {'message': 'Ocorrencia não encontrada'}, 404
