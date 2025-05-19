-- Criação do Banco
CREATE DATABASE IF NOT EXISTS elemento_x_supplements;
USE elemento_x_supplements;

-- Tabela de Produtos
CREATE TABLE produtos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL CHECK (preco > 0),
    estoque INT NOT NULL DEFAULT 0,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nome (nome)
);

-- Tabela de Pedidos com Relacionamento
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    data_pedido DATE NOT NULL,
    status ENUM('pendente', 'processado', 'cancelado') DEFAULT 'pendente',
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    INDEX idx_data (data_pedido)
);

-- Dados Iniciais
INSERT INTO produtos (nome, preco, estoque) VALUES 
('Whey Protein', 129.90, 20),
('Creatina Monohidratada', 89.50, 15),
('Pré-Treino Hardcore', 99.99, 10);

INSERT INTO pedidos (produto_id, quantidade, data_pedido) VALUES
(1, 2, CURDATE()),
(2, 1, CURDATE() - INTERVAL 1 DAY),
(3, 3, CURDATE() - INTERVAL 2 DAY);
