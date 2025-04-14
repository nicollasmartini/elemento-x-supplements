-- Consulta Complexa
SELECT p.nome AS produto, 
       SUM(ped.quantidade) AS total_vendido,
       (ped.quantidade * p.preco) AS valor_total
FROM pedidos ped
JOIN produtos p ON ped.produto_id = p.id
WHERE ped.data_pedido BETWEEN '2025-04-01' AND '2025-04-30'
GROUP BY p.nome
ORDER BY total_vendido DESC;

-- Atualização com Condição
UPDATE produtos 
SET preco = preco * 0.9  -- 10% de desconto
WHERE estoque > 15;

-- Exclusão Segura
DELETE FROM pedidos
WHERE status = 'cancelado' 
AND data_pedido < CURDATE() - INTERVAL 1 YEAR;
