import csv
import requests
from bs4 import BeautifulSoup

# Step 1: Install the necessary libraries
# pip install csv
# pip install requests
# pip install BeautifulSoup4

# Step 2: Send a GET request to the page URL
page_url = "https://sites.google.com/view/tendenciadeprecipitacao/paginainicial"
response = requests.get(page_url)
# print(response)

# Step 3: Parse the HTML content and locate the first iframe element
soup = BeautifulSoup(response.content, "html.parser")
outer_iframe = soup.find("iframe")

## get parent element from outer_iframe
data_url = outer_iframe.find_parent("div", {"data-url": True})["data-url"]

print(data_url)

# Step 4: Send a GET request to the inner iframe URL
response = requests.get(data_url)

# Step 5: Parse the HTML content and find the table element
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table")
print(table)

# Step 6: Extract the table data and insert it into a CSV file
rows = table.find_all("tr")
with open("table.csv", "w", newline="") as csvFile:
    writer = csv.writer(
        csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for i, row in enumerate(rows):
        if i > 6:
            break
        cols = row.find_all("td")
        row_data = []
        for j, col in enumerate(cols):
            if j == 6:
                continue
            if j > 9:
                break
            row_data.append(col.text.strip())
        print("\t".join(row_data))
        writer.writerow(row_data)

## Step 7: Insert the retrieved data into the database
# Configuração de conexão com o banco de dados MariaDB
import mysql.connector

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

    # Loop para enviar cada valor da metropolitana separadamente
    for i, valor in enumerate(metropolitana):
        # Pega os valores min e max para o valor atual
        min_value = 0
        max_value = 0
        if valor == "Sem chuva":
            min_value = 0
            max_value = 2
        elif valor == "Fraca":
            min_value = 2
            max_value = 10
        elif valor == "Fraca a moderada":
            min_value = 10
            max_value = 30
        elif valor == "Moderada":
            min_value = 30
            max_value = 50
        elif valor == "Moderada a forte":
            min_value = 50
            max_value = 100
        elif valor == "Forte":
            min_value = 101
            max_value = 200

        # Cria a tupla com os valores da metropolitana
        tupla = (data[i], metropolitana[i], min_value, max_value)

        # Adiciona a tupla à lista de dados
        dados.append(tupla)

# SQL para inserir os valores na tabela
sql = "INSERT INTO tendencia (data, metropolitana, min, max) VALUES (%s, %s, %s, %s)"

# Executa o insert para todos os valores
cursor.executemany(sql, dados)

# Confirma a inserção dos dados no banco de dados
mydb.commit()

# Fecha a conexão com o banco de dados
mydb.close()
