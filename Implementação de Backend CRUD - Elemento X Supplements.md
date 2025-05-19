# Implementação de Backend CRUD - Elemento X Supplements

Este documento descreve as alterações realizadas no projeto Elemento X Supplements para implementar um backend com operações CRUD (Create, Read, Update, Delete) conforme solicitado pelo professor.

## Visão Geral das Alterações

O projeto original consistia apenas de páginas HTML estáticas que utilizavam localStorage para gerenciar o carrinho de compras, sem comunicação com banco de dados. As alterações implementadas incluem:

1. Criação de um backend em Flask que se comunica com o banco de dados SQLite
2. Implementação de API REST para operações CRUD de produtos e pedidos
3. Modificação das páginas HTML para consumir a API via JavaScript
4. Adição de interface administrativa para gerenciamento de produtos
5. Implementação de histórico de pedidos

## Arquivos Modificados

### Backend
- **app.py**: Novo arquivo contendo toda a lógica do backend em Flask, incluindo rotas para API REST e conexão com o banco de dados.

### Frontend
- **index.html**: Modificado para carregar produtos do banco de dados via API.
- **produtos.html**: Modificado para incluir interface administrativa CRUD e carregar produtos do banco de dados.
- **carrinho.html**: Modificado para finalizar compras via API e exibir histórico de pedidos.

## Como Executar o Projeto

1. Certifique-se de ter o Python e o Flask instalados:
   ```
   pip install flask
   ```

2. Coloque todos os arquivos (HTML e app.py) no mesmo diretório, junto com o banco de dados SQLite.

3. Execute o servidor Flask:
   ```
   python app.py
   ```

4. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Funcionalidades Implementadas

### API REST para Produtos
- GET /api/produtos - Lista todos os produtos
- GET /api/produtos/{id} - Obtém um produto específico
- POST /api/produtos - Cria um novo produto
- PUT /api/produtos/{id} - Atualiza um produto existente
- DELETE /api/produtos/{id} - Exclui um produto

### API REST para Pedidos
- GET /api/pedidos - Lista todos os pedidos
- GET /api/pedidos/{id} - Obtém um pedido específico
- POST /api/pedidos - Cria um novo pedido
- PUT /api/pedidos/{id} - Atualiza um pedido existente
- DELETE /api/pedidos/{id} - Exclui um pedido
- POST /api/finalizar-compra - Finaliza uma compra com múltiplos itens

### Interface Administrativa
- Adicionada na página de produtos (produtos.html)
- Permite criar, visualizar, editar e excluir produtos
- Acesso via botão "Mostrar Administração"

### Histórico de Pedidos
- Adicionado na página do carrinho (carrinho.html)
- Exibe todos os pedidos realizados, com detalhes de produto, quantidade, data e valor

## Observações Importantes

1. O banco de dados é inicializado automaticamente se não existir.
2. O carrinho ainda utiliza localStorage para armazenamento temporário, mas ao finalizar a compra, os dados são enviados para o backend e salvos no banco de dados.
3. A interface administrativa é simplificada para fins didáticos, em um ambiente de produção seria necessário implementar autenticação.
