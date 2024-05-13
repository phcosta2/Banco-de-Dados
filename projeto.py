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


with open("DDL.sql", "r") as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
cursor.execute(sql_script)

# Commit the changes (if necessary)
conexao.commit()

# Close the cursor and the connection
cursor.close()
conexao.close()




# Arrumar a quantidade de caracteres dentro do varchar
# Remover o ID horas de chave primária em horas complementares (ele pode ser repetido)
# Perguntar se pode utilizar o python para inserir dados
# Perguntar sobre os dados null
