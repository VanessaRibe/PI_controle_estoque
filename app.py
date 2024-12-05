from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Usuario, Produto
from database import init_db

app = Flask(__name__)
init_db(app)  # Inicializa o banco de dados com a instância do Flask

app.secret_key = 'ea9139fba29ba0956a9fe84be5f707dd'  # Chave secreta para sessões

@app.template_filter('currency')
def currency_format(value):
    return f'R$ {value:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # Lógica de autenticação do usuário
    username = request.form['username']
    password = request.form['password']
    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and usuario.password == password:
        session['user_id'] = usuario.id
        return redirect(url_for('inicio'))
    return 'Usuário ou senha inválidos'

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        # Lógica para registrar novo usuário
        username = request.form['username']
        password = request.form['password']
        novo_usuario = Usuario(username=username, password=password)
        db.session.add(novo_usuario)
        db.session.commit()
        session['user_id'] = novo_usuario.id
        return redirect(url_for('inicio'))
    return render_template('registrar.html')

@app.route('/inicio')
def inicio():
    if 'user_id' in session:
        produtos = Produto.query.all()
        return render_template('inicio.html', produtos=produtos)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        produtos = Produto.query.all()
        return render_template('dashboard.html', produtos=produtos)
    return redirect(url_for('login'))

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if 'user_id' in session:
        if request.method == 'POST':
            # Lógica para adicionar produto
            nome = request.form['nome']
            preco = request.form['preco']
            quantidade = request.form['quantidade']
            produto = Produto(nome=nome, preco=preco, quantidade=quantidade)
            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('adicionar_produto.html')
    return redirect(url_for('login'))

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar_produto(id):
    if 'user_id' in session:
        produto = Produto.query.get(id)
        if request.method == 'POST':
            # Lógica para atualizar produto
            produto.nome = request.form['nome']
            produto.preco = request.form['preco']
            produto.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('atualizar_produto.html', produto=produto)
    return redirect(url_for('login'))

@app.route('/remover/<int:id>')
def remover_produto(id):
    if 'user_id' in session:
        produto = Produto.query.get(id)
        db.session.delete(produto)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/relatorios')
def relatorios():
    if 'user_id' in session:
        produtos = Produto.query.all()
        return render_template('relatorios.html', produtos=produtos)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

