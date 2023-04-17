import csv
from sys import displayhook
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# # Step 4: Interact with the inner iframe using Selenium
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(data_url)

# Step 5: Find the table element
table = driver.find_element(By.TAG_NAME, "table")
print(table)
rows = table.find_elements(By.TAG_NAME, "tr")

## Step 6: Insert the retrieved data inside a csv file
with open("table.csv", "w", newline="") as csvFile:
    writer = csv.writer(
        csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    for i, row in enumerate(rows):
        if i > 6:
            break
        cols = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        for j, col in enumerate(cols):
            if j > 7:
                break
            row_data.append(col.text.strip())
        print("\t".join(row_data))
        writer.writerow(row_data)

## Step 7: Close the browser
driver.quit()

###############################################################################################

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
        elif i == 2:
            matanorte = row[1:6]
        elif i == 3:
            metropolitana = row[1:6]
        elif i == 4:
            matasul = row[1:6]
        elif i == 5:
            agreste = row[1:6]
        elif i == 6:
            sertao = row[1:6]

# Cria as tuplas com os valores de cada região
for i in range(5):
    tupla = (data[i], matanorte[i], metropolitana[i], matasul[i], agreste[i], sertao[i])
    dados.append(tupla)

# SQL para inserir os valores na tabela
sql = "INSERT INTO novodados (data, matanorte, metropolitana, matasul, agreste, sertao) VALUES (%s, %s, %s, %s, %s, %s)"
print("dados inseridos")
# Executa o insert para todos os valores
cursor.executemany(sql, dados)

# Confirma a inserção dos dados no banco de dados
mydb.commit()

# Fecha a conexão com o banco de dados
mydb.close()
