from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do Flask
app = Flask(__name__)
CORS(app)

@app.route("/megasena", methods=["GET"])
def megasena():
    # Configurar o navegador em modo headless
    options = Options()
    options.headless = True

    # Configurar o WebDriver do Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Acessar o site
        driver.get("https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
