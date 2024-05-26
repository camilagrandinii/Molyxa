# Use a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de requirements para o contêiner
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos para o contêiner
COPY . .

# Define a variável de ambiente FLASK_APP
ENV FLASK_APP=app.py

# Expõe a porta 5001 para fora do contêiner
EXPOSE 5000

# Comando a ser executado quando o contêiner for iniciado
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
