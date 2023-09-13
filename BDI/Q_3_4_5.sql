--CONSULTAS SQL SIMPLES E COMPLEXAS EM UM BANCO DE DADOS POSTGRES

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE produtos_categorias (
    produto_id INTEGER REFERENCES produtos(id),
    categoria_id INTEGER REFERENCES categorias(id),
    PRIMARY KEY (produto_id, categoria_id)
);


-- INSERINDO VALORES DE TESTE NAS TABELAS

INSERT INTO produtos (nome, preco)
VALUES
    ('Smartphone', 799.99),
    ('Notebook', 1299.99),
    ('Camiseta', 19.99),
    ('Harry Potter', 35.99);

INSERT INTO categorias (nome)
VALUES
    ('Eletrônicos'),
    ('Roupas'),
    ('Livros'),
	('Cosméticos'); -- Essa categoria ficará vazia


INSERT INTO produtos_categorias (produto_id, categoria_id)
VALUES
    (1, 1), 
    (2, 1), 
    (3, 2),
    (4, 3); -- Não associando nenhum produto a categoria "cosméticos";


--3) Para Listar os nomes de todos os produtos com mais de R$100, 
-- ordenados por preço e nome e mostrando como nome das colunas
-- "Produto" e "valor", temos a seguinte query:

SELECT
    nome AS "Produto",
    preco AS "Valor"
FROM
    produtos 
WHERE
    preco > 100
ORDER BY
    preco, nome;

--4) Para listar os id's e preços dos produtos cujo preço é maior que a média,
--tem-se a seguinte query:

SELECT
    id,
    preco
FROM
    produtos
WHERE
    preco > (SELECT AVG(preco) FROM produtos);
	
--5) O preço médio de produtos por categoria, ordenada por nome e
--excluindo as categorias sem produtos, pode ser consultada pela query:

SELECT
    c.nome AS "Categoria",
    AVG(p.preco) AS "Preço Medio"
FROM
    categorias c
LEFT JOIN
    produtos_categorias pc ON c.id = pc.categoria_id
LEFT JOIN
    produtos p ON pc.produto_id = p.id
GROUP BY
    c.nome
HAVING
    COUNT(p.id) > 0
ORDER BY
    c.nome;


