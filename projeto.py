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

print('Leitura de dados')
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


lista_materias = [num for num in random.sample(range(100000, 999999), 60)]

# Gera 100 números únicos entre 100000000 e 500000000 servir para os RAs dos alunos
ra_aluno = random.sample(range(100000000, 500000000), 10)
# Gera 60 números únicos entre 500000001 e 999999999 servir para os RAs dos profesores
ra_professor = random.sample(range(500000001, 999999999), 10)
# Formata os números no padrão xx.xxx.xxx-x e adicionar na lista com list compehension
ids_aluno = [f"{str(num)[:2]}.{str(num)[2:5]}.{str(num)[5:8]}-{str(num)[8]}" for num in ra_aluno]
# Formata os números no padrão xx.xxx.xxx-x e adicionar na lista com list compehension
ids_prof = [f"{str(num)[:2]}.{str(num)[2:5]}.{str(num)[5:8]}-{str(num)[8]}" for num in ra_professor]

lista_hist_escolar = [num for num in random.sample(range(1, 500000), 60)]

lista_hist_professor = [num for num in random.sample(range(500001, 999999), 60)]

print('inicialização das listas')


#inicialização dos providers:
fake.add_provider(nome_materia)
fake.add_provider(semestre)

# valores chaves de variaveis para quando for criar valores ficticios
primary_keys = {
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica"],
    "id_curso" : ['MA', 'FI', 'CC', 'EE', 'EM'],
     "id_materia" : ['452645', '745234', '258452', '123254', '123456', '545236'],
}
# criacao da tabelas das horas complementares - id_horas : descricao
tabela_horas = {
    "A1" : "Vistas técnicas monitoras com plano previamente aprovado(empresas, industrias, férias, exposições)",
    "A2" : "Participação como ouvinte em eventos técnico-científicos na área de conhecimento do curso (congresso, seminário, oficina e outros eventos de mesma natureza).", 
    "A3" : "Apresentação de trabalho em eventos técnico-científicos na área de conhecimento do curso (comunicação oral, apresentação de painel, mini-curso, oficina, mesa de debates e outras formas de comunicação previstas).",
    "A4" : "Participação em atividade acadêmicas oferecidas no âmbito do próprio curso (semana de atividades ou jornada de estudo, outros eventos de mesma natureza).",
    "A5" : "Cursos extracurriculares e de extensão (curso de língua estrangeira, informática, capacitação, outros cursos de mesma natureza).",
    "A6" : "Projetos acadêmicos multidisciplinares (projeto institucional de pesquisa, temático, de competição, desenvolvimento de protótipos).",
    "A7" : "Projetos institucionais de iniciação científica, iniciação didática e de ações sociais e extensão (P-BIC, PRO-BID E PRO-BASE).",
    "A8" : "Monitoria ou tutoria na instituição.",
    "A9" : "Publicação de carácter técnico, científico em livros e revistas indexadas.",
    "A10" : "Publicação em anais de eventos técnicos-científicos",
    "A11" : "Publicação em congressos de iniciação cientifica",
    "A12" : "Organização de congressos, seminários, oficinas, semanas de estudos e demais eventos de natureza acadêmico-cientifica.",
    "A13" : "Participação em projetos, programas e ações comunitárias e de extensão universitária desenvolvidas pela instituição.",
    "A14" : "Participação em órgãos de representação estudantil (D.A., DCE, Atlética)",
    "A15" : "Participação em colegiados de curso e superiores da instituição.",
    "A16" : "Estágio extracurricular e atividade profissionais, remunerados ou não, com funções correlatas às competências do curso.",
    "A17" : "Participação orientada em atividades culturais (cinema, teatro, música e dança) com temas pertinentes aos conteúdos do curso.",
    "A18" : "Participação como ouvinte ou convidado em Bancas de Mestrado ou Doutorado na instituição ou em outra que possua programa de pós-graduação reconhecido pelo CAPES.",
    "A19" : "Participação em atividade esportivas oficiais externas, representando o município, o estado, o país ou a instituição, ou internas providas pela própria instituição.",
    "A20" : "Curso Básico de Língua Brasileira de Sinais (LIBRAS)",
    "A21" : "Diretoria de Empresa Júnior"
}

#Criação das tabela de departamento:
for linha in range(len(primary_keys["nome_departamento"])):
    cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", (
    primary_keys["nome_departamento"][linha],
    fake.first_name()
    ))#TABELA COMPLETA


# Criação das tabelas do Professor
for linha in range(len(ids_prof)):
    cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s,%s)", (
    ids_prof[linha], 
    fake.first_name(), 
    random.randint(2000,20000),
    random.choice(primary_keys["nome_departamento"])
    ))#TABELA COMPLETA

#Criação das tabelas da Materia:
for linha in range(len(lista_materias)):
    cursor.execute("INSERT INTO MATERIA VALUES (%s, %s, %s,%s)", (
    lista_materias[linha], 
    fake.materias(), 
    fake.pybool(), 
    ids_prof[random.randint(0, (len(ids_prof)-1))]
    ))#TABELA INCOMPLETA

# PRECISA ESCREVER O NOME DE DEPARTAMENTO CORRETO NA MATÉRIA BASEADO NO QUE ESTA NA TABELA DO PROFESSOR
cursor.execute("SELECT id_professor, nome_departamento FROM PROFESSOR")
professores = cursor.fetchall() 
for _ in professores:
    cursor.execute("UPDATE MATERIA SET nome_departamento = %s WHERE id_professor = %s", (_[1], _[0]))


#Criação da Tabela Curso:
for linha in range(len(primary_keys["id_curso"])):
    cursor.execute("INSERT INTO CURSO (id_curso, horas_extras) VALUES (%s, %s)", (
    primary_keys["id_curso"][linha] ,
    random.randint(160,300)
    ))#TABELA INCOMPLETA
#FALTOU NOME DO CURSO E NOME DO DEPARTAMENTO
#1) 
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



#Criação da tabela Matriz Curricular
for materia in lista_materias:
    cursor.execute("INSERT INTO MATRIZ_CURRICULAR (id_materia) VALUES (%s)", (
        str(materia),
        ))#TABELA INCOMPLETA

# PRECISA ESCREVER O NOME DO DEPARTAMENTO BASEADO NO ID_MATERIA PRESENTE EM MATERIA

# Atualizar a tabela de matérias com o departamento baseado no id do prof
#Escrever materia e id_curso em matriz curricular puxando da materia
cursor.execute("SELECT id_materia, nome_departamento FROM MATERIA")
materiaa = cursor.fetchall() #criar tupla com todos os dados da tabela
for _ in materiaa:
    cursor.execute("UPDATE MATRIZ_CURRICULAR SET materia = %s WHERE id_materia = %s", (_[1], _[0]))

cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'MA' WHERE materia = 'Matemática'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'FI' WHERE materia = 'Física'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'CC' WHERE materia = 'Ciência da Computação'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'EE' WHERE materia = 'Engenharia Elétrica'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'EM' WHERE materia = 'Engenharia Mecânica'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'EQ' WHERE materia = 'Engenharia Química'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'AD' WHERE materia = 'Administração'")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'EP' WHERE materia = 'Engenharia de Produção' ")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'EN' WHERE materia = 'Engenharia Nuclear' ")
cursor.execute("UPDATE MATRIZ_CURRICULAR SET id_curso = 'ET' WHERE materia = 'Engenharia Textil'")

#Criação das tabelas do TCC: - precisa colocar titulos decentes
for linha in range(len(ids_aluno)):
    cursor.execute("INSERT INTO TCC (titulo,id_professor) VALUES (%s,%s)", (
        "Título " + str(linha),
          ids_prof[random.randint(0, (len(ids_prof)-1))]
          ))#TABELA COMPLETA

#Criação das tabelas do Aluno:
for linha in range(len(ids_aluno)):
    cursor.execute("INSERT INTO ALUNO (id_aluno, nome_aluno, idade_aluno, id_curso, id_tcc) VALUES (%s, %s, %s, %s, %s)", (
        ids_aluno[linha], 
        fake.first_name(), 
        random.randint(18,65),
        primary_keys["id_curso"][random.randint(0, 4)], 
        (linha + 1)
        ))#TABELA COMPLETA
  

#<VERIFICADO ATÉ ESSE PONTO por Pedro>


#Criação da tabela de Horas Complementares
for linha in range(len(ids_aluno)):
    aux = random.randint(1, 20)
    string = 'A' + str(aux)
    cursor.execute("INSERT INTO HORAS_COMPLEMENTARES (id_horas, descricao, horas_extras, id_aluno) VALUES (%s, %s, %s, %s)", (
        string, 
        tabela_horas[string], 
        random.randint(4, 31), 
        ids_aluno[random.randint(0, (len(ids_aluno)-1))]
        ))

#Criação das tabelas Histórico Escolar - PRECISA ARRUMAR - o mesmo aluno esta com ids de histotico diferentes, precisa ser igual
for linha in range(len(lista_hist_escolar)):
    cursor.execute("INSERT INTO HISTORICO_ESCOLAR (id_historico_escolar, nota, semestre, ano, id_aluno, id_materia) VALUES(%s, %s, %s, %s, %s, %s)", (
        lista_hist_escolar[linha],
        random.randint(0,10),
        fake.semestres(), 
        2020, #random.randint(2000,2020), 
        ids_aluno[random.randint(0, (len(ids_aluno)-1))], 
        lista_materias[random.randint(0, (len(lista_materias)-1))]
        ))

#Criação da tabela Histórico Professor - PRECISA ARRUMAR o mesmo professor esta com ids de histotico diferentes, precisa ser igual e a meteria que ele esta dando no momento nao esta indo para o historico de materias dadas por ele
for linha in range(len(lista_hist_professor)):
    cursor.execute("INSERT INTO HISTORICO_PROFESSOR (id_historico_professor, semestre, ano, quantidade_aulas, id_professor, id_materia) VALUES(%s, %s, %s, %s, %s, %s)", (
        lista_hist_professor[linha],
        fake.semestres(),
        2020, #random.randint(2000, 2020), 
        random.randint(1, 100), 
        ids_prof[random.randint(0, (len(ids_prof)-1))],
        lista_materias[random.randint(0, (len(lista_materias)-1))]
        ))






# criacao das queries
# 1- histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
# query1 = """
#     CREATE VIEW query1 AS
#         SELECT m.id_materia, m.nome_materia, he.semestre, he.ano, he.nota 
#         FROM historico_escolar he
#         INNER JOIN materia m ON he.id_materia = m.id_materia
# """
# cursor.execute(query1)

# query1_1 = """
#     CREATE VIEW query1_1 AS
#         WITH qualquer_pessoa AS (
#             SELECT nome_aluno
#             FROM aluno
#             ORDER BY RANDOM()
#             LIMIT 1
#         )
#         SELECT a.nome_aluno, m.id_materia, m.nome_materia, he.semestre, he.ano, he.nota 
#         FROM historico_escolar he
#         INNER JOIN materia m ON he.id_materia = m.id_materia
#         INNER JOIN aluno a ON a.id_aluno = he.id_aluno
#         WHERE a.nome_aluno = (
#             SELECT nome_aluno
#             FROM qualquer_pessoa
#         )
# """
# cursor.execute(query1_1)

# # 2- histórico de disciplinas ministradas por qualquer professor, com semestre e ano
# query2 = """
#     CREATE VIEW query2 AS 
#         WITH qualquer_professor AS (
#             SELECT nome_professor
#             FROM professor
#             ORDER BY RANDOM()
#             LIMIT 1
#         )
#         SELECT p.nome_professor, hp.id_materia, hp.semestre, hp.ano
#         FROM professor p 
#         INNER JOIN historico_professor hp ON p.id_professor = hp.id_professor
#         WHERE p.nome_professor = (
#             SELECT nome_professor
#             FROM qualquer_professor
#         )
# """
# cursor.execute(query2)

# # 3- listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
# query3 = """
#     CREATE VIEW query3 AS
#         WITH qualquer AS (
#             SELECT semestre, ano
#             FROM historico_escolar
#             ORDER BY RANDOM()
#             LIMIT 1
#         )
#         SELECT a.nome_aluno, c.nome_curso, c.id_curso, he.nota, he.semestre, he.ano
#         FROM aluno a
#         INNER JOIN curso c ON a.id_curso = c.id_curso
#         INNER JOIN historico_escolar he ON a.id_aluno = he.id_aluno 
#         WHERE he.semestre = (
#             SELECT semestre
#             FROM qualquer
#         ) AND he.ano = (
#             SELECT ano
#             FROM qualquer
#         ) AND he.nota >= 5
# """
# cursor.execute(query3)

# # 4- listar todos os professores que são chefes de departamento, junto com o nome do departamento
cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", ('Astrofisica', 'Julia'))
cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s, %s)", ('12.456.789-0', 'Julia', 25000, 'Astrofisica'))
# query4 = """
#     CREATE VIEW query4 AS
#         SELECT p.nome_professor, d.nome_departamento
#         FROM professor p
#         INNER JOIN departamento d ON p.nome_departamento = d.nome_departamento
#         WHERE p.nome_professor = d.chefe_departamento
# """
# cursor.execute(query4)

# # 5- saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
# query5 = """
#     CREATE VIEW query5 AS
#         SELECT a.nome_aluno, p.nome_professor
#         FROM aluno a
#         INNER JOIN tcc t ON t.id_tcc = a.id_tcc 
#         INNER JOIN professor p ON p.id_professor = t.id_professor
# """
# cursor.execute(query5)

with open("query.sql", "r") as sql_file:
    sql_script = sql_file.read()

# executar o SQL script
cursor.execute(sql_script)



conexao.commit()
print("Sucesso")
cursor.close()
conexao.close()