from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# Configuração do banco de dados
DB_PATH = 'elemento_x_supplements.db'

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Função para inicializar o banco de dados se não existir
def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Criar tabela de produtos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
        ''')
        
        # Criar tabela de pedidos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data_pedido TEXT NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
        ''')
        
        # Inserir dados iniciais se a tabela estiver vazia
        cursor.execute('SELECT COUNT(*) FROM produtos')
        if cursor.fetchone()[0] == 0:
            produtos_iniciais = [
                ('ElementoX Whey Protein Isolate', 149.90, 20),
                ('ElementoX Pre-Workout Extreme', 89.90, 15),
                ('ElementoX BCAA 2:1:1 - 60 caps', 69.90, 10),
                ('ElementoX Creatina Monohidratada', 99.90, 25)
            ]
            cursor.executemany('INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)', produtos_iniciais)
        
        conn.commit()
        conn.close()

# Inicializar o banco de dados
init_db()

# Rota para servir a página inicial
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Rota para servir a página de produtos
@app.route('/produtos.html')
def produtos_page():
    return app.send_static_file('produtos.html')

# Rota para servir a página de carrinho
@app.route('/carrinho.html')
def carrinho_page():
    return app.send_static_file('carrinho.html')

# API CRUD para Produtos

# Listar todos os produtos
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    
    return jsonify([dict(produto) for produto in produtos])

# Obter um produto específico
@app.route('/api/produtos/<int:id>', methods=['GET'])
def get_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if produto is None:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify(dict(produto))

# Criar um novo produto
@app.route('/api/produtos', methods=['POST'])
def create_produto():
    if not request.json or not 'nome' in request.json or not 'preco' in request.json:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    nome = request.json['nome']
    preco = request.json['preco']
    estoque = request.json.get('estoque', 0)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)',
                  (nome, preco, estoque))
    conn.commit()
    
    # Obter o ID do produto recém-criado
    produto_id = cursor.lastrowid
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(produto)), 201

# Atualizar um produto existente
@app.route('/api/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if produto is None:
        conn.close()
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Obter dados atualizados ou manter os existentes
    nome = request.json.get('nome', produto['nome'])
    preco = request.json.get('preco', produto['preco'])
    estoque = request.json.get('estoque', produto['estoque'])
    
    conn.execute('UPDATE produtos SET nome = ?, preco = ?, estoque = ? WHERE id = ?',
                (nome, preco, estoque, id))
    conn.commit()
    
    produto_atualizado = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify(dict(produto_atualizado))

# Excluir um produto
@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    
    if produto is None:
        conn.close()
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Produto excluído com sucesso'})

# API CRUD para Pedidos

# Listar todos os pedidos
@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    conn = get_db_connection()
    pedidos = conn.execute('''
        SELECT p.*, pr.nome as produto_nome, pr.preco
        FROM pedidos p
        JOIN produtos pr ON p.produto_id = pr.id
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(pedido) for pedido in pedidos])

# Obter um pedido específico
@app.route('/api/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    conn = get_db_connection()
    pedido = conn.execute('''
        SELECT p.*, pr.nome as produto_nome, pr.preco
        FROM pedidos p
        JOIN produtos pr ON p.produto_id = pr.id
        WHERE p.id = ?
    ''', (id,)).fetchone()
    conn.close()
    
    if pedido is None:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    return jsonify(dict(pedido))

# Criar um novo pedido
@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    if not request.json or not 'produto_id' in request.json or not 'quantidade' in request.json:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    produto_id = request.json['produto_id']
    quantidade = request.json['quantidade']
    data_pedido = request.json.get('data_pedido', datetime.now().strftime('%Y-%m-%d'))
    
    conn = get_db_connection()
    
    # Verificar se o produto existe
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    if produto is None:
        conn.close()
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Verificar estoque
    if produto['estoque'] < quantidade:
        conn.close()
        return jsonify({'error': 'Estoque insuficiente'}), 400
    
    # Atualizar estoque
    conn.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?',
                (quantidade, produto_id))
    
    # Criar pedido
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pedidos (produto_id, quantidade, data_pedido) VALUES (?, ?, ?)',
                  (produto_id, quantidade, data_pedido))
    conn.commit()
    
    # Obter o pedido recém-criado
    pedido_id = cursor.lastrowid
    pedido = conn.execute('''
        SELECT p.*, pr.nome as produto_nome, pr.preco
        FROM pedidos p
        JOIN produtos pr ON p.produto_id = pr.id
        WHERE p.id = ?
    ''', (pedido_id,)).fetchone()
    conn.close()
    
    return jsonify(dict(pedido)), 201

# Atualizar um pedido existente
@app.route('/api/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    conn = get_db_connection()
    pedido = conn.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    
    if pedido is None:
        conn.close()
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    # Obter dados atualizados ou manter os existentes
    produto_id = request.json.get('produto_id', pedido['produto_id'])
    quantidade_antiga = pedido['quantidade']
    quantidade_nova = request.json.get('quantidade', quantidade_antiga)
    data_pedido = request.json.get('data_pedido', pedido['data_pedido'])
    
    # Se o produto_id mudou, verificar se o novo produto existe
    if produto_id != pedido['produto_id']:
        produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
        if produto is None:
            conn.close()
            return jsonify({'error': 'Produto não encontrado'}), 404
    
    # Atualizar estoque (devolver quantidade antiga e retirar nova quantidade)
    conn.execute('UPDATE produtos SET estoque = estoque + ? WHERE id = ?',
                (quantidade_antiga, pedido['produto_id']))
    
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    if produto['estoque'] < quantidade_nova:
        # Reverter a devolução do estoque
        conn.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?',
                    (quantidade_antiga, pedido['produto_id']))
        conn.commit()
        conn.close()
        return jsonify({'error': 'Estoque insuficiente para o novo pedido'}), 400
    
    conn.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?',
                (quantidade_nova, produto_id))
    
    # Atualizar pedido
    conn.execute('UPDATE pedidos SET produto_id = ?, quantidade = ?, data_pedido = ? WHERE id = ?',
                (produto_id, quantidade_nova, data_pedido, id))
    conn.commit()
    
    pedido_atualizado = conn.execute('''
        SELECT p.*, pr.nome as produto_nome, pr.preco
        FROM pedidos p
        JOIN produtos pr ON p.produto_id = pr.id
        WHERE p.id = ?
    ''', (id,)).fetchone()
    conn.close()
    
    return jsonify(dict(pedido_atualizado))

# Excluir um pedido
@app.route('/api/pedidos/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    conn = get_db_connection()
    pedido = conn.execute('SELECT * FROM pedidos WHERE id = ?', (id,)).fetchone()
    
    if pedido is None:
        conn.close()
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    # Devolver quantidade ao estoque
    conn.execute('UPDATE produtos SET estoque = estoque + ? WHERE id = ?',
                (pedido['quantidade'], pedido['produto_id']))
    
    # Excluir pedido
    conn.execute('DELETE FROM pedidos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Pedido excluído com sucesso'})

# Finalizar compra (criar múltiplos pedidos)
@app.route('/api/finalizar-compra', methods=['POST'])
def finalizar_compra():
    if not request.json or not 'itens' in request.json:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    itens = request.json['itens']
    data_pedido = datetime.now().strftime('%Y-%m-%d')
    
    conn = get_db_connection()
    pedidos_criados = []
    
    try:
        for item in itens:
            produto_id = item.get('produto_id')
            quantidade = item.get('quantidade', 1)
            
            if not produto_id:
                raise ValueError('ID do produto não fornecido')
            
            # Verificar se o produto existe
            produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
            if produto is None:
                raise ValueError(f'Produto com ID {produto_id} não encontrado')
            
            # Verificar estoque
            if produto['estoque'] < quantidade:
                raise ValueError(f'Estoque insuficiente para o produto {produto["nome"]}')
            
            # Atualizar estoque
            conn.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?',
                        (quantidade, produto_id))
            
            # Criar pedido
            cursor = conn.cursor()
            cursor.execute('INSERT INTO pedidos (produto_id, quantidade, data_pedido) VALUES (?, ?, ?)',
                          (produto_id, quantidade, data_pedido))
            
            # Obter o pedido recém-criado
            pedido_id = cursor.lastrowid
            pedido = conn.execute('''
                SELECT p.*, pr.nome as produto_nome, pr.preco
                FROM pedidos p
                JOIN produtos pr ON p.produto_id = pr.id
                WHERE p.id = ?
            ''', (pedido_id,)).fetchone()
            
            pedidos_criados.append(dict(pedido))
        
        conn.commit()
        
    except ValueError as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Erro ao processar a compra'}), 500
    
    conn.close()
    return jsonify({'message': 'Compra finalizada com sucesso', 'pedidos': pedidos_criados}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
