DROP DATABASE IF EXISTS projeto;

CREATE DATABASE projeto;

CREATE TABLE IF NOT EXISTS Departamento(
    nome_departamento varchar(50) PRIMARY KEY,
    chefe_departamento varchar(50)
);

CREATE TABLE IF NOT EXISTS Curso(
    id_curso varchar(2) PRIMARY KEY,
    nome_curso varchar(50),
    horas_extras numeric(3),
    nome_departamento varchar(50) REFERENCES Departamento(nome_departamento)
);

CREATE TABLE IF NOT EXISTS Professor(
    id_professor varchar(12) PRIMARY KEY,
    nome_professor varchar(50),
    salario numeric DEFAULT 0,
    nome_departamento varchar(50) REFERENCES Departamento(nome_departamento)
);

CREATE TABLE IF NOT EXISTS Materia(
    id_materia varchar(6) PRIMARY KEY,
    nome_materia varchar(50),
    prova boolean,
    id_professor varchar(12) REFERENCES Professor(id_professor),
    nome_departamento varchar(50) REFERENCES Departamento(nome_departamento)
);

CREATE TABLE IF NOT EXISTS Matriz_Curricular(
    materia varchar(50),
    id_curso varchar(2) REFERENCES Curso(id_curso),
    id_materia varchar(6) REFERENCES Materia(id_materia)
);

CREATE SEQUENCE sequencia_tcc START 1;  
CREATE TABLE IF NOT EXISTS Tcc (
    id_tcc numeric(6) DEFAULT nextval ('sequencia_tcc') PRIMARY KEY,
    titulo varchar(90) NOT NULL,
    id_professor varchar(12) REFERENCES Professor(id_professor)
);

CREATE TABLE IF NOT EXISTS Aluno(
    id_aluno varchar(12) PRIMARY KEY,
    nome_aluno varchar(50),
    idade_aluno numeric(3),
    id_curso varchar(2) REFERENCES Curso(id_curso),
    id_tcc numeric(6) REFERENCES Tcc(id_tcc)
);

CREATE TABLE IF NOT EXISTS Horas_Complementares(
    id_horas varchar(3), --*
    descricao varchar(220),
    horas_extras numeric(3),
    id_aluno varchar(12) REFERENCES Aluno(id_aluno)
);

CREATE SEQUENCE sequencia_historico_escolar START 1;
CREATE TABLE IF NOT EXISTS Historico_Escolar(
    id_historico_escolar numeric(6) DEFAULT nextval ('sequencia_historico_escolar') PRIMARY KEY,
    nota numeric(2),
    semestre varchar(15),
    ano numeric(4),
    id_aluno varchar(12) REFERENCES Aluno(id_aluno),
    id_materia varchar(6) REFERENCES Materia(id_materia)
);

CREATE SEQUENCE sequencia_historico_professor START 1;
CREATE TABLE IF NOT EXISTS Historico_Professor(
    id_historico_professor numeric(6) DEFAULT nextval('sequencia_historico_professor') PRIMARY KEY,
    semestre varchar(15),
    ano numeric(4),
    quantidade_aulas numeric(4),
    id_professor varchar(12) REFERENCES Professor(id_professor),
    id_materia varchar(6) REFERENCES Materia(id_materia)
);