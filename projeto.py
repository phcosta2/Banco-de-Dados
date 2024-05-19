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

lista_materias = []
for i in range(60):
    materia = random.randint(100000, 999999)
    if materia not in lista_materias:
        lista_materias.append(materia)


# adicionando RA's de alunos aleatoriamente e concatenando eles posteriormente
aux_ids_aluno = []
ids_aluno = []

for i in range(100):
    num = random.randint(100000000, 500000000)
    if num not in aux_ids_aluno:
        aux_ids_aluno.append(str(num))

for id in aux_ids_aluno:
    id = id[0:2] + '.' + id[2:5] + '.' + id[5:8] + '-' + id[8]
    ids_aluno.append(id)

# adicionando RA's de professores aleatoriamente e concatenando eles posteriormente
aux_ids_prof = []
ids_prof = []

for i in range(60):
    num = random.randint(500000001, 999999999)
    if num not in aux_ids_prof:
        aux_ids_prof.append(str(num))

for id in aux_ids_prof:
    id = id[0:2] + '.' + id[2:5] + '.' + id[5:8] + '-' + id[8]
    ids_prof.append(id)


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
    "nome_departamento" : ["Matemática", "Física", "Ciência da Computação", "Engenharia Elétrica", "Engenharia Mecânica"],
     "id_professor" : ["12.244.524-8", "12.244.785-4", "12.244.132-8", "12.244.512-4", "12.244.654-7", "12.244.368-2", "12.244.524-3", "12.244.952-4", "12.244.714-2", "12.244.518-4"],
     "id_aluno" : ['24.122.055-7', '24.122.027-6', '24.122.049-9','24.122.011-2','24.122.024-4','24.122.088-8','24.122.088-2', '24.122.099-9','24.122.011-1','24.122.000-1'],
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
    cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", (primary_keys["nome_departamento"][linha],  fake.first_name()))

# Criação das tabelas do Professor
for linha in range(len(ids_prof)):
    cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s,%s)", (ids_prof[linha], fake.first_name(), random.randint(2000,20000),random.choice(primary_keys["nome_departamento"])))

#Criação das tabelas da Materia:
for linha in range(len(lista_materias)):
    cursor.execute("INSERT INTO MATERIA VALUES (%s, %s, %s,%s)", (lista_materias[linha], fake.materias(), fake.pybool(), ids_prof[random.randint(0, 59)]))
# primary_keys["id_materia"][linha]

#Criação da Tabela Curso:
for linha in range(len(primary_keys["id_curso"])):
    cursor.execute("INSERT INTO CURSO VALUES (%s, %s, %s)", (primary_keys["id_curso"][linha] ,'Null', random.randint(160,300)))


#Criação da tabela Matriz Curricular -  MATRIZ CURRICULAR E MATERIA PRECISA ARRUMAR, ELES PRECISAM ESTAR NO MESMO DEPARTAMENTO, O QUE NAO ESTA ACONTECENDO DEVIDO A GERACAO DE IDS DE MANEIRA ALEATORIA
for linha in range(len(primary_keys["nome_departamento"])): 
    for i in range(len(primary_keys["id_materia"])):
        cursor.execute("INSERT INTO MATRIZ_CURRICULAR VALUES (%s,%s, %s)", (primary_keys["nome_departamento"][linha], primary_keys["id_curso"][linha], lista_materias[linha]))


#Criação das tabelas do TCC: - precisa colocar titulos decentes
for linha in range(100):
    cursor.execute("INSERT INTO TCC (titulo,id_professor) VALUES (%s,%s)", ("Título " + str(linha), ids_prof[random.randint(0, 59)]))

#Criação das tabelas do Aluno:
for linha in range(len(ids_aluno)):
    cursor.execute("INSERT INTO ALUNO (id_aluno, nome_aluno, idade_aluno, id_curso, id_tcc) VALUES (%s, %s, %s, %s, %s)", (ids_aluno[linha], fake.first_name(), random.randint(18,65), primary_keys["id_curso"][random.randint(0, 4)], (linha + 1)))


#Criação da tabela de Horas Complementares
for linha in range(len(ids_aluno)):
    aux = random.randint(1, 20)
    string = 'A' + str(aux)
    cursor.execute("INSERT INTO HORAS_COMPLEMENTARES (id_horas, descricao, horas_extras, id_aluno) VALUES (%s, %s, %s, %s)", (string, tabela_horas[string], random.randint(4, 31), ids_aluno[random.randint(0, 99)]))

#Criação das tabelas Histórico Escolar - PRECISA ARRUMAR - o mesmo aluno esta com ids de histotico diferentes, precisa ser igual
for linha in range(100):
   cursor.execute("INSERT INTO HISTORICO_ESCOLAR (nota, semestre, ano,id_aluno,id_materia) VALUES(%s,%s,%s,%s,%s)", (random.randint(0,10), fake.semestres(), random.randint(2000,2020), ids_aluno[random.randint(0, 99)], lista_materias[random.randint(0, 59)]))

#Criação da tabela Histórico Professor - PRECISA ARRUMAR o mesmo professor esta com ids de histotico diferentes, precisa ser igual e a meteria que ele esta dando no momento nao esta indo para o historico de materias dadas por ele
for linha in range(100):
    cursor.execute("INSERT INTO HISTORICO_PROFESSOR (semestre, ano, quantidade_aulas, id_professor, id_materia) VALUES(%s, %s, %s, %s, %s)", (fake.semestres(), random.randint(2000, 2020), random.randint(1, 100), ids_prof[random.randint(0, 59)], lista_materias[random.randint(0, 59)]))

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