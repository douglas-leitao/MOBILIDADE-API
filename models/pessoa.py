from sql_alchemy import banco
from datetime import date
import dateparser

class PersonModel(banco.Model):
    __tablename__ = 'pessoas'

    person_id = banco.Column(banco.String, primary_key=True)
    cpf = banco.Column(banco.String(11))
    rg = banco.Column(banco.String(10), unique=True)
    uf_rg = banco.Column(banco.String(2))
    nome = banco.Column(banco.String(100))
    data_nasc = banco.Column(banco.String(10))
    idade = banco.Column(banco.String(3))
    sexo = banco.Column(banco.String(1))
    # HABILITACAO
    n_registro = banco.Column(banco.String(11), unique=True)
    uf_reg = banco.Column(banco.String(2))
    cat_hab = banco.Column(banco.String(5))
    validade = banco.Column(banco.String(10))
    primeira_hab = banco.Column(banco.String(10))
    # CONTATOS
    telefone = banco.Column(banco.String(13))
    email = banco.Column(banco.String(50))
    #cep = banco.Column(banco.String(10))
    # ENDERECO
    logradouro = banco.Column(banco.String(100))
    log_nro = banco.Column(banco.String(8))
    complemento = banco.Column(banco.String(20))
    bairro = banco.Column(banco.String(100))
    cidade = banco.Column(banco.String(100))
    uf = banco.Column(banco.String(2))

    def __init__(self, person_id, cpf, rg,  nome, data_nasc, sexo, telefone, email, uf_rg, n_registro, uf_reg, validade, cat_hab,  primeira_hab, logradouro, log_nro, complemento, bairro, cidade, uf):
        self.person_id = person_id
        self.cpf = cpf
        self.rg = rg
        self.uf_rg = uf_rg
        self.nome = nome
        self.data_nasc = data_nasc
        #today = date.today()
        #dt_nasc = dateparser.parse(data_nasc, '%d/%m/%y')
        #self.idade = today.year - dt_nasc.year - ((today.month, today.day) < (dt_nasc.month, dt_nasc.day))
        self.sexo = sexo
        #
        self.n_registro = n_registro
        self.uf_reg = uf_reg
        self.cat_hab = cat_hab
        self.validade = validade
        self.primeira_hab = primeira_hab
        #
        self.telefone = telefone
        self.email = email
        self.logradouro = logradouro
        self.log_nro = log_nro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

    def json(self):
        return {
            'person_id': self.person_id,
            'cpf': self.cpf,
            'rg': self.rg,
            'uf_rg': self.uf_rg,
            'nome': self.nome,
            'data_nasc': self.data_nasc,
            'sexo': self.sexo,
            #
            'n_registro': self.n_registro,
            'uf_reg': self.uf_reg,
            'cat_hab': self.cat_hab,
            'validade': self.validade,
            'primeira_hab': self.primeira_hab,
            #
            'telefone': self.telefone,
            'email': self.email,
            'logradouro': self.logradouro,
            'log_nro': self.log_nro,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'uf': self.uf
        }

    @classmethod
    def find_person(cls, person_id):
        pessoa = cls.query.filter_by(person_id = person_id).first()
        if pessoa:
            return pessoa
        return None

    @classmethod
    def find_by_cpf(cls, cpf_informado):
        print('testando cpf')
        print(cpf_informado)
        pessoa = cls.query.filter_by(cpf = cpf_informado).first()
        if pessoa:
            return pessoa
        return None

    def find_rg(cls, rg):
        pessoa = cls.query.filter_by(rg = rg).first()
        if pessoa:
            return pessoa
        return None

    def find_registro(cls, n_registro):
        pessoa = cls.query.filter_by(n_registro = n_registro).first()
        if pessoa:
            return pessoa
        return None

    def save_person(self):
        banco.session.add(self)
        banco.session.commit()

    def update_person(self, cpf, rg, uf_rg, nome, data_nasc, sexo, telefone, email, n_registro, uf_reg, validade, cat_hab,  primeira_hab, logradouro, log_nro, complemento, bairro, cidade, uf):
        self.cpf = cpf
        self.rg = rg
        self.uf = uf_rg
        self.nome = nome
        self.data_nasc = data_nasc
        #today = date.today()
        #dt_nasc = dateparser.parse(data_nasc, '%d/%m/%y')
        #self.idade = today.year - dt_nasc.year - ((today.month, today.day) < (dt_nasc.month, dt_nasc.day))
        self.sexo = sexo
        #
        self.n_registro = n_registro
        self.uf_reg = uf_reg
        self.cat_hab = cat_hab
        self.validade = validade
        self.primeira_hab = primeira_hab
        #
        self.telefone = telefone
        self.email = email
        self.logradouro = logradouro
        self.log_nro = log_nro
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf

    def delete_person(self):
        banco.session.delete(self)
        banco.session.commit()

    def calculate_age(born):
        print(born)
        today = date.today()
        print(today)
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
