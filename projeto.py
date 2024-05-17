import psycopg2
import json
from faker import Faker
from faker.providers import DynamicProvider
import random
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


with open("DDL.sql", "r") as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
cursor.execute(sql_script)


#Criação dos dados nas tabelas:


# Crie uma instância do Faker em pt-br
fake = Faker('pt-br')
# Gerar um nome de departamento aleatorio
nome_materia = DynamicProvider(
     provider_name="materias",
     elements=["Calculo 1", "Calculo 2", "Calculo 3", "Calculo 4", "Probabilidade e Estatística", "Desenvolvimento de Projetos", "Introdução a Computação"],
)





#inicialização dos providers:
fake.add_provider(nome_materia)

primary_keys = {
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica", "Engenharia Química", "Administração", "Engenharia de Produção", "Engenharia Nuclear", "Engenharia Textil"],
    "id_professor" : ["12.244.524-8", "12.244.785-4", "12.244.132-8", "12.244.512-4", "12.244.654-7", "12.244.368-2", "12.244.524-3", "12.244.952-4", "12.244.714-2", "12.244.518-4"],
    "id_aluno" : ['24.122.055-7', '24.122.027-6', '24.122.049-9','24.122.011-2','24.122.024-4','24.122.088-8','24.122.088-2', '24.122.099-9','24.122.011-1','24.122.000-1'],
    "id_curso" : ['MA', 'FI', 'CC', 'EE', 'EM', 'EQ', 'AD', 'EP', 'EN', 'ET'],
    "id_materia" : ['MA2645', 'FI5234', 'CC8452', 'EE3254', 'EM8475', 'EQ2147', 'AD6352', 'EP8756', 'EN7832', 'ET1253'],
    "semestre" : ['Primeiro','Segundo','Terceiro','Quarto','Quinto','Sexto','Sétimo','Oitavo','Nono','Décimo']
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
    cursor.execute("INSERT INTO CURSO VALUES (%s, %s, %s)", (primary_keys["id_curso"][linha] , "AAA", random.randint(160,300)))


#Criação das tabelas do TCC:

for linha in range(10):
    cursor.execute("INSERT INTO TCC (titulo,id_professor) VALUES (%s,%s)", ("Título",random.choice(primary_keys['id_professor'])))


#Criação das tabelas do Aluno:

for linha in range(len(primary_keys["id_aluno"])):
    cursor.execute("INSERT INTO ALUNO VALUES (%s, %s, %s)", (primary_keys["id_aluno"][linha], fake.first_name(),random.randint(18,65)))

#Criação fas tabelas Histórico Escolar


for linha in range(10):
    cursor.execute("INSERT INTO HISTORICO_ESCOLAR (nota,semestre,ano,id_aluno,id_materia) VALUES(%s,%s,%s,%s,%s)", (random.randint(0,10),random.choice(primary_keys["semestre"]),random.randint(2000,2030),primary_keys["id_aluno"][linha],primary_keys["id_materia"][linha]))

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

