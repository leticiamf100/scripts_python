import requests
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurações do Supabase
SUPABASE_URL = 'SUPABASE_URL' # Substitua pela url de acesso do Supabase
SUPABASE_KEY = 'SUPABASE_KEY' # Substitua pela sua key de acesso do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurações
ACCESS_TOKEN = 'ACCESS_TOKEN'  # Substitua pelo seu token de acesso do Facebook
AD_ACCOUNT_ID = ['AD_ACCOUNT_ID', # Substitua pelos IDs das contas do Facebook                 
]

BASE_URL = 'https://graph.facebook.com/v16.0'  # Certifique-se de usar a versão correta da API

# Variável global para armazenar os statuses
statuses = {}

# Função para obter o status da conta de anúncios
def get_account_status(ad_account_id):
    url = f'{BASE_URL}/{ad_account_id}'
    params = {
        'fields': 'account_status',
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'account_status' in data:
        return data['account_status']
    else:
        return f"Erro ao obter status da conta {ad_account_id}: {data.get('error', 'Desconhecido')}"

# Função principal para verificar o status de várias contas
@app.route('/ad_accounts/status', methods=['GET'])
def check_all_account_statuses():
    global statuses
    statuses.clear() # Limpa os statuses anteriores
    for ad_account_id in AD_ACCOUNT_ID:
        account_status = get_account_status(ad_account_id)
        statuses[ad_account_id] = account_status
    print(statuses)

@app.route('/ad_accounts/status', methods=['GET'])
def get_all_account_statuses():
    return jsonify(statuses)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_all_account_statuses, 'interval', minutes=1)  # Executa a cada 1 minuto
    scheduler.start()
    app.run(port=5000)
