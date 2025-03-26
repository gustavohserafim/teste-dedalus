import csv
import requests

API_URL = "http://127.0.0.1:8000/api/user"  
CSV_FILE = "usuarios.csv" 

def enviar_requisicao(user_data):
    """Envia uma requisição POST para criar um usuário na API."""
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code == 201:
            print(f"Ok: {user_data['email']} - Usuário criado!")
        else:
            print(f"Falha: {user_data['email']} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Falha ao conectar com a API: {e}")

def processar_csv(arquivo_csv):
    """Lê o arquivo CSV e envia os dados para a API."""
    with open(arquivo_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Lê o CSV como dicionário
        
        for row in reader:
            user_data = {
                "name": row["nome"],
                "email": row["email"],
                "cpf": row["cpf"],
                "birthdate": row["data_nascimento"]
            }
            enviar_requisicao(user_data)

if __name__ == "__main__":
    processar_csv(CSV_FILE)
