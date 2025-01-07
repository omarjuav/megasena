from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import subprocess
import time
import os

# Configuração do Flask
app = Flask(__name__)
CORS(app)

@app.route("/megasena", methods=["GET"])
def megasena():
    # Configurar o navegador em modo headless
    options = Options()
    options.headless = True
    
    # Caso necessário, defina o caminho para o Chromium no Render (se já instalado)
    # options.binary_location = "/usr/bin/chromium"  # Localização do Chromium no Render
    
    # Instalar o driver do Chrome e configurar o serviço
    service = Service(ChromeDriverManager().install())
    
    # Inicializar o WebDriver com o Chrome
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Acessar o site da Mega-Sena
        driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")
        driver.maximize_window()
        time.sleep(10)
        
        # Selecionar os elementos com ng-repeat específico e as classes ng-binding e ng-scope
        elementos = driver.find_elements(
            By.XPATH,
            "//*[contains(@ng-repeat, 'dezena in resultado.listaDezenas') and contains(@class, 'ng-binding') and contains(@class, 'ng-scope')]"
        )

        # Extrair os números
        numeros = [elemento.text for elemento in elementos]

        # Verificar se os números foram encontrados
        if numeros:
            return jsonify({"numeros": numeros})
        else:
            return jsonify({"error": "Números não encontrados na página"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Fechar o navegador
        driver.quit()

# Rota inicial para testar a aplicação
@app.route("/")
def index():
    return "Bem-vindo à MegaSena API!"

if __name__ == "__main__":
    # Obter a porta da variável de ambiente do Render ou usar a porta 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
