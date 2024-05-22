--1- histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
CREATE VIEW query1 AS
    WITH qualquer_pessoa AS (
        SELECT nome_aluno
        FROM aluno
        ORDER BY RANDOM()
        LIMIT 1
    )
    SELECT a.nome_aluno, m.id_materia, m.nome_materia, he.semestre, he.ano, he.nota 
    FROM historico_escolar he
    INNER JOIN materia m ON he.id_materia = m.id_materia
    INNER JOIN aluno a ON a.id_aluno = he.id_aluno
    WHERE a.nome_aluno = (
        SELECT nome_aluno
        FROM qualquer_pessoa
    );

--2- histórico de disciplinas ministradas por qualquer professor, com semestre e ano
CREATE VIEW query2 AS 
    WITH qualquer_professor AS (
        SELECT nome_professor
        FROM professor
        ORDER BY RANDOM()
        LIMIT 1
    )
    SELECT p.nome_professor, hp.id_materia, hp.semestre, hp.ano
    FROM professor p 
    INNER JOIN historico_professor hp ON p.id_professor = hp.id_professor
    WHERE p.nome_professor = (
        SELECT nome_professor
        FROM qualquer_professor
    );

--3- listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
CREATE VIEW query3 AS
    WITH qualquer AS (
        SELECT semestre, ano
        FROM historico_escolar
        ORDER BY RANDOM()
        LIMIT 1
    )
    SELECT a.nome_aluno, c.nome_curso, c.id_curso, he.nota, he.semestre, he.ano
    FROM aluno a
    INNER JOIN curso c ON a.id_curso = c.id_curso
    INNER JOIN historico_escolar he ON a.id_aluno = he.id_aluno 
    WHERE he.semestre = (
        SELECT semestre
        FROM qualquer
    ) AND he.ano = (
        SELECT ano
        FROM qualquer
    ) AND he.nota >= 5;

--4- listar todos os professores que são chefes de departamento, junto com o nome do departamento
CREATE VIEW query4 AS
    SELECT p.nome_professor, d.nome_departamento
    FROM professor p
    INNER JOIN departamento d ON p.nome_departamento = d.nome_departamento
    WHERE p.nome_professor = d.chefe_departamento;

--5- saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
CREATE VIEW query5 AS
    SELECT a.nome_aluno, p.nome_professor
    FROM aluno a
    INNER JOIN tcc t ON t.id_tcc = a.id_tcc 
    INNER JOIN professor p ON p.id_professor = t.id_professor;
