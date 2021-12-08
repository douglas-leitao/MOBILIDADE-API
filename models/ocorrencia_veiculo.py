from sql_alchemy import banco


class OcorrenciaVeiculoModel(banco.Model):
    __tablename__ = 'ocorrencia_veiculo'

    ocorrencia_id = banco.Column(banco.String, primary_key=True)
    veiculo_id = banco.Column(banco.String, primary_key=True)
    placa = banco.Column(banco.String(7), unique=True)
    renavan = banco.Column(banco.String(11), unique=True)


    def __init__(self, ocorrencia_id, veiculo_id, placa, renavan):
        self.ocorrencia_id = ocorrencia_id
        self.veiculo_id = veiculo_id
        self.placa = placa
        self.renavan = renavan


    def json(self):
        return {
            'ocorrencia_id': self.ocorrencia_id,
            'veiculo_id': self.veiculo_id,
            'placa': self.placa,
            'renavan': self.renavan,
        }

    @classmethod
    def find_veiculos_ocorrencia(cls, ocorrencia_id, renavan):
        ocorrencia = cls.query.filter_by(ocorrencia_id = ocorrencia_id, renavan = renavan).first()
        if ocorrencia:
            return ocorrencia
        return None

    def save_ocorrencia_veiculo(self):
        banco.session.add(self)
        banco.session.commit()

    def update_ocorrencia_veiculo(self, ocorrencia_id, veiculo_id, placa, renavan):
        self.ocorrencia_id = ocorrencia_id
        self.veiculo_id = veiculo_id
        self.placa = placa
        self.renavan = renavan

    def delete_ocorrencia(self):
        banco.session.delete(self)
        banco.session.commit()
