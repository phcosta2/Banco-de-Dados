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
    "id_materia" : ['CC2645', 'MA5234', 'CC8452', 'FI3254', 'CC8475', 'EQ2147', 'EQ6352', 'ET8756', 'AD7832', 'MA1253']
    
}



#Criação das tabela de departamento:

for linha in range(len(primary_keys["nome_departamento"])):
    cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", (primary_keys["nome_departamento"][linha],  fake.first_name()))

# Criação das tabelas do Professor

for linha in range(len(primary_keys["id_professor"])):
    cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s,%s)", (primary_keys["id_professor"][linha], fake.first_name(), random.randint(2000,20000),random.choice(primary_keys["nome_departamento"])))

#Criação das tabelas da Materia:

for linha in range(len(primary_keys["id_materia"])):
    cursor.execute("INSERT INTO MATERIA VALUES (%s, %s, %s,%s,%s)", (primary_keys["id_materia"][linha], fake.materias(), fake.pybool(),random.choice(primary_keys["id_professor"]),random.choice(primary_keys["nome_departamento"])))



#escrever os dados na tabela:
conexao.commit()


# Arrumar a quantidade de caracteres dentro do varchar
# Remover o ID horas de chave primária em horas complementares (ele pode ser repetido)
# Perguntar se pode utilizar o python para inserir dados
# Perguntar sobre os dados null
