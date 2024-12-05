from flask import Flask
from models import db


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
    app.config['SECRET_KEY'] = 'ea9139fba29ba0956a9fe84be5f707dd'

    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Banco de dados inicializado com sucesso!")
