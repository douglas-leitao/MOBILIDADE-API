from sql_alchemy import banco


class OcorrenciaModel(banco.Model):
    __tablename__ = 'ocorrencias'

    ocorrencia_id = banco.Column(banco.String, primary_key=True)
    data_sinistro = banco.Column(banco.String(10))
    hora_sinistro = banco.Column(banco.String(10))
    cidade = banco.Column(banco.String(100))
    logradouro = banco.Column(banco.String(100))
    log_nro = banco.Column(banco.String(6))
    complemento = banco.Column(banco.String(20))
    bairro = banco.Column(banco.String(100))
    tipo_sinistro = banco.Column(banco.String(20))
    clima = banco.Column(banco.String(20))
    mao_direcao = banco.Column(banco.String(10))
    tipo_pavimento = banco.Column(banco.String(20))
    superficie_pista = banco.Column(banco.String(10))
    controle_trafego = banco.Column(banco.String(20))
    iluminacao = banco.Column(banco.String(20))
    velocidade_via = banco.Column(banco.String(7))


    def __init__(self, ocorrencia_id, data_sinistro, hora_sinistro, cidade, logradouro, log_nro, complemento, bairro, tipo_sinistro, clima, mao_direcao, tipo_pavimento, superficie_pista, controle_trafego,  iluminacao, velocidade_via):
        self.ocorrencia_id = ocorrencia_id
        self.data_sinistro = data_sinistro
        self.hora_sinistro = hora_sinistro
        self.cidade = cidade
        self.logradouro = logradouro
        self.log_nro = log_nro
        self.complemento = complemento
        self.bairro = bairro
        self.tipo_sinistro = tipo_sinistro
        self.clima = clima
        self.mao_direcao = mao_direcao
        self.tipo_pavimento = tipo_pavimento
        self.superficie_pista = superficie_pista
        self.controle_trafego = controle_trafego
        self.iluminacao = iluminacao
        self.velocidade_via = velocidade_via

    def json(self):
        return {
            'ocorrencia_id': self.ocorrencia_id,
            'data_sinistro': self.data_sinistro,
            'hora_sinistro': self.hora_sinistro,
            'cidade': self.cidade,
            'logradouro': self.logradouro,
            'log_nro': self.log_nro,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'tipo_sinistro': self.tipo_sinistro,
            'clima': self.clima,
            'mao_direcao': self.mao_direcao,
            'tipo_pavimento': self.tipo_pavimento,
            'superficie_pista': self.superficie_pista,
            'controle_trafego': self.controle_trafego,
            'iluminacao': self.iluminacao,
            'velocidade_via': self.velocidade_via
        }

    @classmethod
    def find_ocorrencia(cls, ocorrencia_id):
        ocorrencia = cls.query.filter_by(ocorrencia_id = ocorrencia_id).first()
        if ocorrencia:
            return ocorrencia
        return None

    def save_ocorrencia(self):
        banco.session.add(self)
        banco.session.commit()

    def update_ocorrencia(self, data_sinistro, hora_sinistro, cidade, logradouro, log_nro, complemento, bairro, tipo_sinistro, clima, mao_direcao, tipo_pavimento, superficie_pista, controle_trafego,  iluminacao, velocidade_via):
        self.data_sinistro = data_sinistro
        self.hora_sinistro = hora_sinistro
        self.cidade = cidade
        self.logradouro = logradouro
        self.log_nro = log_nro
        self.complemento = complemento
        self.bairro = bairro
        self.tipo_sinistro = tipo_sinistro
        self.clima = clima
        self.mao_direcao = mao_direcao
        self.tipo_pavimento = tipo_pavimento
        self.superficie_pista = superficie_pista
        self.controle_trafego = controle_trafego
        self.iluminacao = iluminacao
        self.velocidade_via = velocidade_via

    def delete_ocorrencia(self):
        banco.session.delete(self)
        banco.session.commit()

