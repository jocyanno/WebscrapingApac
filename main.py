import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

# Mapeamento dos nomes dos meses para números
meses = {
    'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,
    'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8,
    'set': 9, 'out': 10, 'nov': 11, 'dez': 12
}

# Step 1: Install the necessary libraries

# Step 2: Send a GET request to the page URL
page_url = 'https://sites.google.com/view/tendenciadeprecipitacao/paginainicial'
response = requests.get(page_url)
# print(response)

# Step 3: Parse the HTML content and locate the first iframe element
soup = BeautifulSoup(response.content, 'html.parser')
outer_iframe = soup.find('iframe')

## get parent element from outer_iframe
data_url = outer_iframe.find_parent('div', {'data-url': True})['data-url']

print(data_url)

# # Step 4: Interact with the inner iframe using Selenium
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get(data_url)

# Step 5: Find the table element
table = driver.find_element(By.TAG_NAME, 'table')
print(table)
rows = table.find_elements(By.TAG_NAME, 'tr')

## Step 6: Insert the retrieved data inside a csv file
with open('table.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i, row in enumerate(rows):
        if i > 6:
            break
        cols = row.find_elements(By.TAG_NAME, 'td')
        row_data = []
        for j, col in enumerate(cols):
            if j == 6:
                continue
            if j > 9:
                break
            row_data.append(col.text.strip())
        print('\t'.join(row_data))
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
            entrada = row[1:6]
            # Extrai o dia e o mês da entrada
            dia, mes_str = entrada.split()[1].split('/')

            # Remove o zero à esquerda do mês, se houver
            mes_str1 = mes_str.lstrip('0')
            mes =int(mes_str1)

            # Obtém o ano atual
            ano = datetime.datetime.now().year

            # Cria um objeto datetime com a data
            data = datetime.datetime(ano, mes, int(dia))
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
sql = "INSERT INTO novodados (data, metropolitana, min, max) VALUES (%s, %s, %s, %s)"

# Executa o insert para todos os valores
cursor.executemany(sql, dados)

# Confirma a inserção dos dados no banco de dados
mydb.commit()

# Fecha a conexão com o banco de dados
mydb.close()

