from sql_alchemy import banco
from models.ocorrencia_veiculo import OcorrenciaVeiculoModel


class VeiculoModel(banco.Model):
    __tablename__ = 'veiculos'

    veiculo_id = banco.Column(banco.String, primary_key=True)
    placa = banco.Column(banco.String(7), unique=True)
    renavan = banco.Column(banco.String(11), unique=True)
    marca = banco.Column(banco.String(20))
    modelo = banco.Column(banco.String(20))
    ano_modelo = banco.Column(banco.String(4))
    cor = banco.Column(banco.String(10))
    especie = banco.Column(banco.String(10))
    tipo = banco.Column(banco.String(10))
    categoria = banco.Column(banco.String(10))
    proprietario_fk = banco.Column(banco.String(100))

    def __init__(self, veiculo_id, placa, renavan, marca, modelo, ano_modelo, cor, especie, tipo, categoria, proprietario_fk):
        self.veiculo_id = veiculo_id
        self.placa = placa
        self.renavan = renavan
        self.marca = marca
        self.modelo = modelo
        self.ano_modelo = ano_modelo
        self.cor = cor
        self.especie = especie
        self.tipo = tipo
        self.categoria = categoria
        self.proprietario_fk = proprietario_fk

    def json(self):
        return {
            'veiculo_id': self.veiculo_id,
            'placa': self.placa,
            'renavan': self.renavan,
            'marca': self.marca,
            'modelo': self.modelo,
            'ano_modelo': self.ano_modelo,
            'cor': self.cor,
            'especie': self.especie,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'proprietario_fk': self.proprietario_fk
        }

    @classmethod
    def find_veiculo(cls, veiculo_id):
        veiculo = cls.query.filter_by(veiculo_id = veiculo_id).first()
        if veiculo:
            return veiculo
        return None

    @classmethod
    def find_veiculo_placa(cls, placa):
        veiculo = cls.query.filter_by(placa = placa).first()
        if veiculo:
            return veiculo
        return None

    @classmethod
    def find_veiculo_renavan(cls, renavan):
        veiculo = cls.query.filter_by(renavan = renavan).first()
        if veiculo:
            return veiculo
        return None

    def save_veiculo(self):
        banco.session.add(self)
        banco.session.commit()
        #OcorrenciaVeiculoModel.save_ocorrencia_veiculo()
        # testando deploy heroku

    def update_veiculo(self, placa, renavan, marca, modelo, ano_modelo, cor, especie, tipo, categoria, proprietario_fk):
        self.placa = placa
        self.renavan = renavan
        self.marca = marca
        self.modelo = modelo
        self.ano_modelo = ano_modelo
        self.cor = cor
        self.especie = especie
        self.tipo = tipo
        self.categoria = categoria
        self.proprietario_fk = proprietario_fk

    def delete_veiculo(self):
        banco.session.delete(self)
        banco.session.commit()