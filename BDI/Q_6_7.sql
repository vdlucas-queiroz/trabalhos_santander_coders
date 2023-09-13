-- INSERÇÕES, ALTERAÇÕES E REMOÇÕES DE OBJETOS E DADOS EM UM BANDO DE DADOS POSTGRES

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    codigo_turma VARCHAR(20) NOT NULL,
    nome_turma VARCHAR(100) NOT NULL
);

CREATE TABLE aluno (
    id_aluno VARCHAR(11) PRIMARY KEY, --pensei no CPF
    nome_aluno VARCHAR(100) NOT NULL,
    aluno_alocado BOOLEAN,
    id_turma INT,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma)
);

-- a) Inserir pelo menos duas turmas diferentes na tabela de turma;

INSERT INTO turma (codigo_turma, nome_turma)
VALUES
    ('1006', 'Turma A'),
    ('1008', 'Turma B');
	
--b) Inserir pelo menos 1 aluno alocado em cada uma destas
-- turmas na tabela aluno (todos com NULL na coluna aluno_alocado):


INSERT INTO aluno (id_aluno, nome_aluno, aluno_alocado, id_turma)
VALUES
    ('00000000001','Ayrles', NULL, 1),
    ('00000000002','Clovis', NULL, 1),
	('00000000003','Lucas', NULL, 2),
	('00000000004','Afonso', NULL, 2);

--c) Inserir pelo menos 2 alunos não alocados em nenhuma
-- turma na tabela aluno (todos com NULL na coluna aluno_alocado):

INSERT INTO aluno (id_aluno, nome_aluno, aluno_alocado)
VALUES
    ('00000000005','Cleide', NULL),
    ('00000000006','Jussara', NULL);
	
--d) Atualizar a coluna aluno_alocado da tabela aluno, de modo que os alunos associados a uma disciplina recebam o valor True 
-- e alunos não associdos a nenhuma disciplina recebam o falor False para esta coluna.	


UPDATE aluno
SET aluno_alocado = TRUE
WHERE id_turma IS NOT NULL;

UPDATE aluno
SET aluno_alocado = FALSE
WHERE id_turma IS NULL;


-- Observando a tabela depois da atualização:
SELECT * FROM aluno;