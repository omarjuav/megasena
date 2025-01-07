FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libxss1 \
    libappindicator3-1 \
    libindicator3-7 \
    libnspr4 \
    libnss3 \
    fonts-liberation \
    libx11-xcb1 \
    libappindicator1 \
    libxtst6 \
    libgtk-3-0 \
    libgbm1 \
    xdg-utils \
    chromium

# Instalar dependências Python
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copiar o restante do código
COPY . /app

# Definir variável de ambiente para o caminho do Chrome
ENV PATH="/usr/bin/chromium:${PATH}"

# Expor a porta onde o app Flask vai rodar
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
