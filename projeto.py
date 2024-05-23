# import de todas as bibliotecas utilizadas
import psycopg2
import json
from faker import Faker
from faker.providers import DynamicProvider
import random

# Ler os dados do arquivo.json (database,user,password,host,port) e armazená-los na variável config
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
    elements = ['Primeiro', 'Segundo' ,'Terceiro' ,'Quarto' ,'Quinto' ,'Sexto' ,'Sétimo' ,'Oitavo']
)

# gera aleatoriamente e sem repetir o codigo das materias (60)
lista_materias = [num for num in random.sample(range(100000, 999999), 60)]
# gera aleatoriamente e sem repetir o RA dos alunos (50)
ra_aluno = random.sample(range(100000000, 500000000), 50)
# gera aleatoriamente e sem repetir o RA dos professores (20)
ra_professor = random.sample(range(500000001, 999999999), 20)
# Formata os números no padrão xx.xxx.xxx-x e adicionar na lista com list compehension
ids_aluno = [f"{str(num)[:2]}.{str(num)[2:5]}.{str(num)[5:8]}-{str(num)[8]}" for num in ra_aluno]
# Formata os números no padrão xx.xxx.xxx-x e adicionar na lista com list compehension
ids_prof = [f"{str(num)[:2]}.{str(num)[2:5]}.{str(num)[5:8]}-{str(num)[8]}" for num in ra_professor]
# gera aleatoriamente e sem repetir a lista de historico escolar dos alunos (60)
lista_hist_escolar = [num for num in random.sample(range(1, 500000), 60)]
# gera aleatoriamente e sem repetir a lista do historico dos professores (60)
lista_hist_professor = [num for num in random.sample(range(500001, 999999), 60)]

# testar a inicializacao do codigo
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

# criacao da tabela das horas complementares - id_horas : descricao
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
    ))

# Criação das tabelas do Professor
for linha in range(len(ids_prof)):
    cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s,%s)", (
    ids_prof[linha], 
    fake.first_name(), 
    random.randint(2000,20000),
    random.choice(primary_keys["nome_departamento"])
    ))

#Criação das tabelas da Materia:
for linha in range(len(lista_materias)):
    cursor.execute("INSERT INTO MATERIA VALUES (%s, %s, %s,%s)", (
    lista_materias[linha], 
    fake.materias(), 
    fake.pybool(), 
    ids_prof[random.randint(0, (len(ids_prof)-1))]
    ))
    
# atualizar o nome do departamento na tabela materia de acordo com o id do professor
cursor.execute("SELECT id_professor, nome_departamento FROM PROFESSOR")
professores = cursor.fetchall() 
for _ in professores:
    cursor.execute("UPDATE MATERIA SET nome_departamento = %s WHERE id_professor = %s", (_[1], _[0]))

#Criação da Tabela Curso:
for linha in range(len(primary_keys["id_curso"])):
    cursor.execute("INSERT INTO CURSO (id_curso, horas_extras) VALUES (%s, %s)", (
    primary_keys["id_curso"][linha] ,
    random.randint(160,300)
    ))

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
        ))

#Atualizar a tabela de matérias com o departamento baseado no id do prof
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

#Criação das tabelas do TCC:
for linha in range(len(ids_aluno)):
    cursor.execute("INSERT INTO TCC (titulo,id_professor) VALUES (%s,%s)", (
        "Título " + str(linha),
          ids_prof[random.randint(0, (len(ids_prof)-1))]
          ))

#Criação das tabelas do Aluno:
for linha in range(len(ids_aluno)):
    cursor.execute("INSERT INTO ALUNO (id_aluno, nome_aluno, idade_aluno, id_curso, id_tcc) VALUES (%s, %s, %s, %s, %s)", (
        ids_aluno[linha], 
        fake.first_name(), 
        random.randint(18,65),
        primary_keys["id_curso"][random.randint(0, 4)], 
        (linha + 1)
        ))

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

#Criação das tabelas Histórico Escolar
for linha in range(len(lista_hist_escolar)):
    cursor.execute("INSERT INTO HISTORICO_ESCOLAR (id_historico_escolar, nota, semestre, ano, id_aluno, id_materia) VALUES(%s, %s, %s, %s, %s, %s)", (
        lista_hist_escolar[linha],
        random.randint(0,10),
        fake.semestres(), 
        2020, #random.randint(2000,2020), 
        ids_aluno[random.randint(0, (len(ids_aluno)-1))], 
        lista_materias[random.randint(0, (len(lista_materias)-1))]
        ))

#Criação da tabela Histórico Professor
for linha in range(len(lista_hist_professor)):
    cursor.execute("INSERT INTO HISTORICO_PROFESSOR (id_historico_professor, semestre, ano, quantidade_aulas, id_professor, id_materia) VALUES(%s, %s, %s, %s, %s, %s)", (
        lista_hist_professor[linha],
        fake.semestres(),
        2020, #random.randint(2000, 2020), 
        random.randint(1, 100), 
        ids_prof[random.randint(0, (len(ids_prof)-1))],
        lista_materias[random.randint(0, (len(lista_materias)-1))]
        ))

# 4- listar todos os professores que são chefes de departamento, junto com o nome do departamento
cursor.execute("INSERT INTO DEPARTAMENTO VALUES (%s, %s)", ('Astrofisica', 'Julia'))
cursor.execute("INSERT INTO PROFESSOR VALUES (%s, %s, %s, %s)", ('12.456.789-0', 'Julia', 25000, 'Astrofisica'))

# ler o arquivo das querys criadas, alem de executa-lo
with open("query.sql", "r") as sql_file:
    sql_script = sql_file.read()

# executar o SQL script
cursor.execute(sql_script)

# commitar (salvar no banco), printar que deu certo e encerrar conexao
conexao.commit()
print("Sucesso")
cursor.close()
conexao.close()
