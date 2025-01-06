from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_cors import CORS
import time

# Configuração do Flask
app = Flask(__name__)

# Habilitar CORS
CORS(app)

# Endpoint para consulta dos números da Mega-Sena
@app.route("/megasena", methods=["GET"])
def megasena():
    # Configurar o navegador em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Garantir que o navegador será executado sem interface
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    # Inicializar o WebDriver com as opções configuradas
    driver = webdriver.Chrome(options=chrome_options)

    # Remover a propriedade 'webdriver' do navegador para evitar detecção
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Acessar o site
        driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")
        
        # Esperar os elementos carregarem
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[contains(@ng-repeat, 'dezena in resultado.listaDezenas') and contains(@class, 'ng-binding') and contains(@class, 'ng-scope')]")
            )
        )

        # Coletar os números
        elementos = driver.find_elements(By.XPATH, "//*[contains(@ng-repeat, 'dezena in resultado.listaDezenas') and contains(@class, 'ng-binding') and contains(@class, 'ng-scope')]")
        numeros = [elemento.text for elemento in elementos]

        # Retornar os números como JSON
        return jsonify({"numeros": numeros})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Fechar o navegador
        driver.quit()

# Rodar a aplicação
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
