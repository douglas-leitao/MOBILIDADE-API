from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_DOMAIN = 'sandbox55d3cb1e6445493d9483371ac8e25501.mailgun.org	'
MAIL_API_KEY = '59c41f93d0797455d7a744e679aa7635-8b34de1b-bb368259'
FROM_TITLE = 'NO-REPLY'
FROM_MAIL = 'no-reply@restapi.com'

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    ativado = banco.Column(banco.Boolean, default=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)

    def __init__(self, login, senha, ativado, email):
        self.login = login
        self.senha = senha
        self.ativado = ativado
        self.email = email


    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', MAIL_API_KEY),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_MAIL),
                          'to': self.email,
                          'subject': 'Confirmação de Cadastro',
                          'text': 'Confirme se cadastro clicando no link a seguir: {}'.format(link),
                          'html': '<html><p>Confirme seu cadastro clicando no link a seguir:\
                           <a href="{}">CONFIRMAR EMAIL</a></p></html>'.format(link)
                          }
                    )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()


    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()