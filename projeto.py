import psycopg2
import json


with open('acess.json') as file:
    config = json.load(file)


conexao = psycopg2.connect(
    database = config['database'],
    user = config['user'],
    password = config['password'],
    host = config['host'],
    port = config['port']
)

cursor = conexao.cursor()


criar_tabela_departamento = """
CREATE TABLE IF NOT EXISTS Departamento(
    nome_departamento varchar(30) PRIMARY KEY,
    chefe_departamento varchar(20)
);
"""

criar_tabela_professor = """
CREATE TABLE IF NOT EXISTS Professor(
    id_professor varchar(12) PRIMARY KEY,
    nome_professor varchar(20),
    salario FLOAT DEFAULT 0,
    nome_departamento varchar(30) REFERENCES Departamento(nome_departamento)
)
"""
criar_tabela_curso = """
CREATE TABLE IF NOT EXISTS Curso(
    id_curso varchar(2) PRIMARY KEY,
    nome_curso varchar(30),
    horas_extras numeric(3),
    nome_departamento varchar(30) REFERENCES Departamento(nome_departamento)
);
"""
criar_tabela_materia = """
CREATE TABLE IF NOT EXISTS Materia(
    id_materia varchar(6) PRIMARY KEY,
    nome_materia varchar(40),
    prova varchar(15),
    id_professor varchar(12) REFERENCES Professor(id_professor),
    nome_departamento varchar(30) REFERENCES Departamento(nome_departamento)
);
"""

criar_tabela_matriz_curricular = """
CREATE TABLE IF NOT EXISTS Matriz_Curricular(
    semestre varchar(15),
    ano numeric(4),
    dia numeric(2),
    id_materia varchar(6) REFERENCES Materia(id_materia),
    id_curso varchar(2) REFERENCES Curso(id_curso)
);
"""

criar_tabela_tcc = """
CREATE TABLE IF NOT EXISTS Tcc (
    id_tcc varchar(14) PRIMARY KEY,
    titulo varchar(40) NOT NULL,
    id_professor varchar(12) REFERENCES Professor(id_professor)
);
"""

criar_tabela_aluno = """
CREATE TABLE IF NOT EXISTS Aluno(
    id_aluno varchar(12) PRIMARY KEY,
    nome_aluno varchar(20),
    idade_aluno numeric(3),
    id_curso varchar(2) REFERENCES Curso(id_curso),
    id_tcc varchar(14) REFERENCES Tcc(id_tcc)
);
"""

criar_tabela_horas_complementares = """
CREATE TABLE IF NOT EXISTS Horas_Complementares(
    id_horas varchar(3) PRIMARY KEY,
    descricao varchar(80),
    horas_extras numeric(3),
    id_aluno varchar(20) REFERENCES Aluno(id_aluno)
);
"""

criar_tabela_historico_escolar = """
CREATE TABLE IF NOT EXISTS Historico_Escolar(
    id_historico varchar(12) PRIMARY KEY,
    nota numeric(2),
    semestre varchar(15),
    id_aluno varchar(20) REFERENCES Aluno(id_aluno),
    id_materia varchar(6) REFERENCES Materia(id_materia)
);
"""

cursor.execute(criar_tabela_departamento)
cursor.execute(criar_tabela_professor)
cursor.execute(criar_tabela_curso)
cursor.execute(criar_tabela_materia)
cursor.execute(criar_tabela_matriz_curricular)
cursor.execute(criar_tabela_tcc)
cursor.execute(criar_tabela_aluno)
cursor.execute(criar_tabela_horas_complementares)
cursor.execute(criar_tabela_historico_escolar)

cursor.execute("DELETE FROM departamento")
cursor.execute("INSERT INTO DEPARTAMENTO VALUES ('Matematica','Leonardo Anjoletto')")
cursor.execute("INSERT INTO DEPARTAMENTO VALUES ('Ciencias da Computacao','Matheus Gomes')")

cursor.execute("DELETE FROM professor")
cursor.execute("INSERT INTO PROFESSOR VALUES ('123456789','Gustavo',5000)")
cursor.execute("INSERT INTO PROFESSOR VALUES ('987654321','Bruno',2000)")

cursor.execute("DELETE FROM curso")
cursor.execute("INSERT INTO CURSO VALUES ('CC', 'Ciencias da Computacao',260)")
cursor.execute("INSERT INTO CURSO VALUES ('EP', 'Engenharia de Producao',220)")

cursor.execute("DELETE FROM materia")
cursor.execute("INSERT INTO MATERIA VALUES ('CC2648','Banco de Dados','P2')")
cursor.execute("INSERT INTO MATERIA VALUES ('CC1948','Calculo 1','Projeto')")

cursor.execute("DELETE FROM matriz_curricular")
cursor.execute("INSERT INTO MATRIZ_CURRICULAR VALUES ('Segundo',2024,12)")
cursor.execute("INSERT INTO MATRIZ_CURRICULAR VALUES ('Primeiro',2023,1)")

cursor.execute("DELETE FROM tcc")
cursor.execute("INSERT INTO TCC VALUES ('1224058962','Conhecimentos de Banco de Dados')")
cursor.execute("INSERT INTO TCC VALUES ('122402','Conhecimentos de Redes')")

cursor.execute("DELETE FROM aluno")
cursor.execute("INSERT INTO ALUNO VALUES ('24.122.027-6','João',19)")
cursor.execute("INSERT INTO ALUNO VALUES ('24.122.055-7','Felipe',21)")

cursor.execute("DELETE FROM horas_complementares")
cursor.execute("INSERT INTO HORAS_COMPLEMENTARES VALUES ('A05','curso de banco de dados',50)")
cursor.execute("INSERT INTO HORAS_COMPLEMENTARES VALUES ('A03','curso de Redes',30)")

cursor.execute("DELETE FROM historico_escolar")
cursor.execute("INSERT INTO HISTORICO_ESCOLAR VALUES ('12212121',10,'quinto')")
cursor.execute("INSERT INTO HISTORICO_ESCOLAR VALUES ('1222',7,'segundo')")




conexao.commit()


# Arrumar a quantidade de caracteres dentro do varchar
# Remover o ID horas de chave primária em horas complementares (ele pode ser repetido)
# Perguntar se pode utilizar o python para inserir dados
# Perguntar sobre os dados null