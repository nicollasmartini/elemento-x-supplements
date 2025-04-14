CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER NOT NULL
);


INSERT INTO produtos (nome, preco, estoque) VALUES 
('Whey Protein', 129.90, 20),
('Creatina Monohidratada', 89.50, 15),
('Pré-Treino Hardcore', 99.99, 10);


CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data_pedido TEXT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);


INSERT INTO pedidos (produto_id, quantidade, data_pedido) VALUES
(1, 2, '2025-04-14'),
(2, 1, '2025-04-13'),
(3, 3, '2025-04-12');
