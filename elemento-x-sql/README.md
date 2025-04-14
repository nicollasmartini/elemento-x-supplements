# 💾 Banco de Dados - Elemento X Supplements

Este repositório contém a modelagem e o script do banco de dados utilizado no projeto **Elemento X Supplements**, uma aplicação web para uma loja de suplementos esportivos de minha autoria para fins de aprendizado.

## 🗂️ Estrutura do Repositório

- `banco.sql`: Script com comandos SQL para criação e inserção de dados nas tabelas `produtos` e `pedidos`.
- `elemento_x_supplements.db`: Arquivo do banco de dados SQLite gerado a partir do script SQL, pronto para ser visualizado e utilizado.

## 🧱 Tabelas Criadas

### 📦 produtos

| Campo     | Tipo    | Descrição                        |
|-----------|---------|----------------------------------|
| id        | INTEGER | Chave primária (autoincremento) |
| nome      | TEXT    | Nome do suplemento               |
| preco     | REAL    | Preço do produto                 |
| estoque   | INTEGER | Quantidade em estoque           |

### 🧾 pedidos

| Campo        | Tipo    | Descrição                               |
|--------------|---------|------------------------------------------|
| id           | INTEGER | Chave primária (autoincremento)         |
| produto_id   | INTEGER | Chave estrangeira → produtos(id)        |
| quantidade   | INTEGER | Quantidade comprada                     |
| data_pedido  | TEXT    | Data do pedido (formato ISO 8601)       |

## 🛠️ Como visualizar o banco

Você pode visualizar o conteúdo do arquivo `.db` com o [DB Browser for SQLite](https://sqlitebrowser.org) maneira que eu utilizei:

1. Abra o programa.
2. Vá em "Abrir Banco de Dados" e selecione `elemento_x_supplements.db`.
3. Use as abas "Procurar Dados" ou "Executar SQL" para explorar o banco.

## 💡 Observações

- Este projeto foi desenvolvido como parte do **Projeto Integrador II** do curso de Tecnologia da Informação da UFMS.
- O banco de dados é simples e focado em aprendizado de modelagem relacional e versionamento de código.

## 📝 Licença

Uso livre para fins educacionais e acadêmicos.
