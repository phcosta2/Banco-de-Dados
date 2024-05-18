# import de todas as bibliotecas utilizadas
import psycopg2
import json
from faker import Faker
from faker.providers import DynamicProvider
import random
with open('acess.json') as file:
    config = json.load(file)


# passar os dados do banco para variaveis
conexao = psycopg2.connect(
    database = config['database'],
    user = config['user'],
    password = config['password'],
    host = config['host'],
    port = config['port']
)

# cursor sera usado para executar tarefas em sql
cursor = conexao.cursor()

# ler o arquivo sql
with open("DDL.sql", "r") as sql_file:
    sql_script = sql_file.read()

# executar o SQL script
cursor.execute(sql_script)


#Criação dos dados nas tabelas:


##criacao da instancia do Faker para pt-br
fake = Faker('pt-br')

# Geracao de nomes de departamento de maneira aleatoria
nome_materia = DynamicProvider(
    provider_name = "materias",
    elements = ["Calculo 1", "Calculo 2", "Calculo 3", "Calculo 4", "Probabilidade e Estatística", "Desenvolvimento de Projetos", "Introdução a Computação"],
)

# Geracao de semestres do historico do professor de maneira aleatoria
semestre = DynamicProvider(
    provider_name = "semestres",
    elements = ['Primeiro', 'Segundo' ,'Terceiro' ,'Quarto' ,'Quinto' ,'Sexto' ,'Sétimo' ,'Oitavo' ,'Nono' ,'Décimo']
)

# # Geracao de semestres do historico escolar de maneira aleatoria
# semestre = DynamicProvider(
#     provider_name="historico_escolar",
#     elements = ['Primeiro', 'Segundo' ,'Terceiro' ,'Quarto' ,'Quinto' ,'Sexto' ,'Sétimo' ,'Oitavo' ,'Nono' ,'Décimo']
# )

#inicialização dos providers:
fake.add_provider(nome_materia)
fake.add_provider(semestre)

# valores chaves de variaveis para quando for criar valores ficticios
primary_keys = {
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica", "Engenharia Química", "Administração", "Engenharia de Produção", "Engenharia Nuclear", "Engenharia Textil"],
    "id_professor" : ["12.244.524-8", "12.244.785-4", "12.244.132-8", "12.244.512-4", "12.244.654-7", "12.244.368-2", "12.244.524-3", "12.244.952-4", "12.244.714-2", "12.244.518-4"],
    "id_aluno" : ['24.122.055-7', '24.122.027-6', '24.122.049-9','24.122.011-2','24.122.024-4','24.122.088-8','24.122.088-2', '24.122.099-9','24.122.011-1','24.122.000-1'],
    "id_curso" : ['MA', 'FI', 'CC', 'EE', 'EM', 'EQ', 'AD', 'EP', 'EN', 'ET'],
    "id_materia" : ['452645', '745234', '258452', '123254', '368475', '522147', '216352', '318756', '917832', '471253'],
}

#Criação das tabela de departamento:
for linha in range(len(primary_keys["nome_departamento"])):
    cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", (primary_keys["nome_departamento"][linha],  fake.first_name()))

# Criação das tabelas do Professor
for linha in range(len(primary_keys["id_professor"])):
    cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s,%s)", (primary_keys["id_professor"][linha], fake.first_name(), random.randint(2000,20000),random.choice(primary_keys["nome_departamento"])))

#Criação das tabelas da Materia:
for linha in range(len(primary_keys["id_materia"])):
    cursor.execute("INSERT INTO MATERIA VALUES (%s, %s, %s,%s)", (primary_keys["id_materia"][linha], fake.materias(), fake.pybool(),random.choice(primary_keys["id_professor"])))

#Criação da Tabela Curso:
for linha in range(len(primary_keys["id_curso"])):
    cursor.execute("INSERT INTO CURSO VALUES (%s, %s, %s)", (primary_keys["id_curso"][linha] ,'Null', random.randint(160,300)))

#Criação da tabela Matriz Curricular


#Criação das tabelas do TCC:
for linha in range(10):
    cursor.execute("INSERT INTO TCC (titulo,id_professor) VALUES (%s,%s)", ("Título " + str(linha),random.choice(primary_keys['id_professor'])))

#Criação das tabelas do Aluno:
for linha in range(len(primary_keys["id_aluno"])):
    cursor.execute("INSERT INTO ALUNO VALUES (%s, %s, %s)", (primary_keys["id_aluno"][linha], fake.first_name(),random.randint(18,65)))

#Criação da tabela de Horas Complementares


#Criação das tabelas Histórico Escolar
for linha in range(len(primary_keys["id_aluno"])):
    cursor.execute("INSERT INTO HISTORICO_ESCOLAR (nota, semestre, ano,id_aluno,id_materia) VALUES(%s,%s,%s,%s,%s)", (random.randint(0,10),fake.semestres(),random.randint(2000,2030),primary_keys["id_aluno"][linha],primary_keys["id_materia"][linha]))

#Criação da tabela Histórico Professor
for linha in range(len(primary_keys["id_professor"])):
    cursor.execute("INSERT INTO HISTORICO_PROFESSOR (semestre, ano, quantidade_aulas, id_professor) VALUES(%s, %s, %s, %s)", (fake.semestres(), random.randint(2000, 2030), random.randint(1, 100), primary_keys["id_professor"][linha]))

# id_historico_professor numeric(6) DEFAULT nextval('sequencia_historico_professor') PRIMARY KEY,
#     semestre varchar(15),
#     ano numeric(4),
#     quantidade_aulas numeric(4),
#     id_professor varchar(12) REFERENCES Professor(id_professor),
#     id_materia varchar(6) REFERENCES Materia(id_materia)

#Escrever o nome de departamento da tabela professor
cursor.execute("SELECT id_professor, nome_departamento FROM PROFESSOR")
professores = cursor.fetchall() #criar tupla com todos os dados da tabela


# Atualizar a tabela de matérias com o departamento baseado no id do prof
for professor in professores:
    id_professor = professor[0]
    departamento_professor = professor[1]
    cursor.execute("UPDATE MATERIA SET nome_departamento = %s WHERE id_professor = %s", (departamento_professor, id_professor))

#Atualizar a tabela curso com departamento, nome e id
cursor.execute("UPDATE CURSO SET nome_departamento = 'Matemática' WHERE id_curso = 'MA'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Física' WHERE id_curso = 'FI'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Ciência da Computação' WHERE id_curso = 'CC'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia Elétrica' WHERE id_curso = 'EE'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia Mecânica' WHERE id_curso = 'EM'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia Química' WHERE id_curso = 'EQ'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Administração' WHERE id_curso = 'AD'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia de Produção' WHERE id_curso = 'EP'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia Nuclear' WHERE id_curso = 'EN'")
cursor.execute("UPDATE CURSO SET nome_departamento = 'Engenharia Textil' WHERE id_curso = 'ET'")

# atualizar o nome do curso para ter o mesmo nome do departamento
cursor.execute("UPDATE CURSO SET nome_curso = 'Matemática' WHERE NOME_DEPARTAMENTO = 'Matemática'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Física' WHERE NOME_DEPARTAMENTO = 'Física'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Ciência  Computação' WHERE NOME_DEPARTAMENTO = 'Ciência da Computação'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia Elétrica' WHERE NOME_DEPARTAMENTO = 'Engenharia Elétrica'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia Mecânica' WHERE NOME_DEPARTAMENTO = 'Engenharia Mecânica'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia Química' WHERE NOME_DEPARTAMENTO = 'Engenharia Química'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Administração' WHERE NOME_DEPARTAMENTO = 'Administração'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia de Produção' WHERE NOME_DEPARTAMENTO = 'Engenharia de Produção'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia Nuclear' WHERE NOME_DEPARTAMENTO = 'Engenharia Nuclear'")
cursor.execute("UPDATE CURSO SET nome_curso = 'Engenharia Textil' WHERE NOME_DEPARTAMENTO = 'Engenharia Textil'")


#Escrever o nome de departamento da tabela professor
#cursor.execute("SELECT id_materia, id_professor FROM MATERIA")
#materias = cursor.fetchall() #criar tupla com todos os dados da tabela

# Atualizar a tabela de matérias com o departamento baseado no id do prof
#for materia in materias:
#    id_materia = materia[0]
#    id_professor = materia[1]
#    cursor.execute("UPDATE HISTORICO_PROFESSOR SET id_materia_atual = %s WHERE id_professor = %s", (id_materia, id_professor))




'''
cursor.execute("SELECT id_materia, nome_departamento FROM MATERIA")
materias = cursor.fetchall() #criar tupla com todos os dados da tabela
for element in materias:
    print (element)
    id_mat = element[0]
    departamento_materia = element[1]
    cursor.execute("UPDATE CURSO SET id_materia = %s WHERE nome_departamento = %s", (id_mat, departamento_materia))
'''

#escrever os dados na tabela:
conexao.commit()

