import csv
import mysql.connector

# Configuração de conexão com o banco de dados MariaDB
mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="APAC"
)

# Cria um cursor para executar comandos SQL
cursor = mydb.cursor()

# Lista para armazenar as tuplas com os dados
dados = []

with open("table.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')

    for i, row in enumerate(reader):
        if i == 1:
            data = row[1:6]
        elif i == 3:
            metropolitana = row[1:6]
    
# Cria as tuplas com os valores de cada região
for i in range(5):
    tupla = (data[i], metropolitana[i])
    dados.append(tupla)

# SQL para inserir os valores na tabela
sql = "INSERT INTO tendencia (data,metropolitana) VALUES (%s, %s)"
print("dados inseridos")
# Executa o insert para todos os valores
cursor.executemany(sql, dados)

# Confirma a inserção dos dados no banco de dados
mydb.commit()

# Fecha a conexão com o banco de dados
mydb.close()