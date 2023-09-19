import pandas as pd
import openai
import requests



sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = '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'
openai.api_key = openai_api_key
df = pd.read_csv('SDW2023.csv')
users_ids = df['UserId'].tolist()

def get_user(id):
    response = requests.get(f'{sdw2023_api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in users_ids if (user := get_user(id)) is not None]

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = [
            {
                'role':'system',
                'content':'Você é um especialitsta em marketing bancário senior'
            },
            {
                'role':'system',
                'content':f"Crie uma mensagem curta para {user['name']} sobre a importância de controle financeiro (Máximo 100 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')

for user in users:
    news = generate_ai_news(user)
    print(news)