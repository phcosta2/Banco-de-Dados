# Projeto Banco de Dados
 Projetar uma faculdade utilizando banco de dados para salvar os dados.

# Integrantes
Felipe Orlando Lanzara R.A.: 24.122.055-7

João Vitor Governatore R.A.: 24.122.027-6

Pedro Henrique Lega Kramer Costa R.A.: 24.122.049-0

# Diagrama Relacional(MER)
![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Diagrama%20Relacional%20(MER).png)

# Passos para executar o programa
- Antes de fazer o download do arquivo zip do projeto, deve-se primeiro, fazer a instalação das bibliotecas ```psycopg2``` e ```Faker``` através do comando ```pip install```
- Criar um ```acess.json``` com as seguintes instruções (o nome do ```database``` deve ser "projeto"):

![image](https://github.com/jvgoverna/Projeto-Banco-de-Dados/blob/main/Imagem%20do%20acess%20do%20json.png)

# Explicação das querys:
- Query 1: Dentre todos os alunos que foram colocados aleatoriamente, um deles será escolhido (também aleatoriamente)
- Query 2: Dentre todos os professores que foram colocados aleatoriamente, um deles será escolhido (também aleatoriamente)
- Query 3: Dentre todos os anos (pré-definido como 2020 para facilitar) e semestres (indo de 'Primeiro' até 'Oitavo') que foram colocados aleatoriamente, um de cada será escolhido (também aleatoriamente). Caso o aluno apresente uma nota maior do que a média (5), ele será aprovado.
- Query 4: No modelo de faculdade optamos pelo chefe de departamento não necessáriamente lecionar aulas, visto que seu papel principal é organizar o seu respectivo departamento. Por isso, tanto o nome dos professores, quanto o nome dos chefes de departamento são escolhidos aleatoriamente, tornando as chances deles coincidirem é muito baixa. Por conta desse fator, adicionamos manualmente uma nova professora (Julia), que também será chefe de um novo departamento (Astrofísica), apenas para demonstrar que a query de fato funciona. (Esse departamente e professora foram exclusivamentes criados para essa querry, em outros itens não há o departamento de astrofísica )
- Query 5: Todos os alunos terão um id de TCC já definido junto a um professor que será o orientador.
