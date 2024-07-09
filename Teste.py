from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import time
from Info import regions
import pandas as pd

# Configuração do WebDriver
service = EdgeService()
options = webdriver.EdgeOptions()
# options.add_argument('headless')  # Descomente para executar em modo headless

driver = webdriver.Edge(service=service, options=options)

# Definição das variáveis
origens = [
    "Feira de Santana, Bahia"
    # "Vitória da Conquista, Bahia",
    # "Barreiras, Bahia",
    # "Juazeiro, Bahia",
    # "Serrinha, Bahia",
    # "Itabuna, Bahia",
    # "Salvador, Bahia"
]

# Obter todos os destinos de todas as regiões da Bahia do dicionário regions
destinos = []
for regiao, cidades in regions.items():
    destinos += cidades

# Lista para armazenar os resultados
resultados = []

# Loop para cada combinação de origem e destino
for origem in origens:
    for destino in destinos:
        try:
            # Abrir página inicial do Google Maps com a rota entre origem e destino
            driver.get(f"https://www.google.com/maps/dir/{origem}/{destino}")

            # Aguardar até que o botão de direções esteja clicável
            wait = WebDriverWait(driver, 15)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[2]/button')))
            element.click()

            # Preencher o campo de origem
            origem_input = driver.find_element(By.XPATH, '//*[@id="sb_ifc50"]/input')
            origem_input.clear()
            origem_input.send_keys(origem)

            # Preencher o campo de destino
            destino_input = driver.find_element(By.XPATH, '//*[@id="sb_ifc51"]/input')
            destino_input.clear()
            destino_input.send_keys(destino)
            destino_input.send_keys(Keys.ENTER)

            # Aguardar até que a distância da rota seja carregada
            distancia = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div')))
            distancia_texto = distancia.text
            print(f"Distância de {origem} para {destino}: {distancia_texto}")

            # Aguardar tempo suficiente para o observer capturar as mudanças (ajuste conforme necessário)
            time.sleep(10)

                # Armazenar o resultado na lista
            resultados.append({
                'Origem': origem,
                'Destino': destino,
                'Distância': distancia_texto
            })

        except Exception as e:
            print(f"Erro ao calcular a rota de {origem} para {destino}: {str(e)}")


driver.quit()


df = pd.DataFrame(resultados)

# Salvar em  Excel
nome_arquivo = 'distancias_rotas.xlsx'
df.to_excel(nome_arquivo, index=False)

print(f"Resultados salvos em '{nome_arquivo}'")
