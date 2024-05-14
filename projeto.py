import psycopg2
import json
from faker import Faker
from faker.providers import DynamicProvider

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
nome_departamento = DynamicProvider(
     provider_name="dept_name",
     elements=["Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecãnica", "Engenharia Química", "Administração"],
)

#inicialização dos providers:

fake.add_provider(nome_departamento)


#tabela departamento:
cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", (fake.dept_name(),fake.first_name()))








#escrever os dados na tabela:
conexao.commit()


# Arrumar a quantidade de caracteres dentro do varchar
# Remover o ID horas de chave primária em horas complementares (ele pode ser repetido)
# Perguntar se pode utilizar o python para inserir dados
# Perguntar sobre os dados null
