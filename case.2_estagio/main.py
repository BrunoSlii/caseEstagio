import os
from dotenv import load_dotenv
import requests
from openai import OpenAI


#Chaves API
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

#Estado --> Cidade representativa
STATE_TO_CITY = {
    "são paulo": "São Paulo",
    "rio de janeiro": "Rio de Janeiro",
    "minas gerais": "Belo Horizonte",
    "bahia": "Salvador",
    "pernambuco": "Recife",
    "ceará": "Fortaleza",
    "paraná": "Curitiba",
    "santa catarina": "Florianópolis",
    "rio grande do sul": "Porto Alegre",
    "goiás": "Goiânia",
    "distrito federal": "Brasília",
    "amazonas": "Manaus",
    "pará": "Belém",
    "mato grosso": "Cuiabá",
    "mato grosso do sul": "Campo Grande",
    "espírito santo": "Vitória",
    "maranhão": "São Luís",
    "rio grande do norte": "Natal",
    "paraíba": "João Pessoa",
    "alagoas": "Maceió",
    "sergipe": "Aracaju",
    "piauí": "Teresina",
    "rondônia": "Porto Velho",
    "acre": "Rio Branco",
    "roraima": "Boa Vista",
    "tocantins": "Palmas",
    "amapá": "Macapá"
}

def get_representative_city(state_name: str) -> str:
    """
    Recebe o nome do estado digitado pelo usuário e retorna a cidade
    representativa correspondente. Se não encontrar, retorna o próprio estado.
    """
    key = state_name.strip().lower()
    return STATE_TO_CITY.get(key, state_name)


#Clima cidade 
def get_weather(city_name: str) -> str:
    """
    Consulta a API do OpenWeatherMap para obter dados de clima de uma cidade.
    Retorna um resumo amigável incluindo temperatura, descrição do tempo,
    velocidade do vento e volume de chuva na última hora.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{city_name},BR",
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  
        "lang": "pt"        
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        vento = data["wind"]["speed"]
        chuva = data.get("rain", {}).get("1h", 0)  

        resumo = (
            f"Clima em {city_name}: {desc}, "
            f"temperatura {temp}°C, vento {vento} m/s, "
            f"chuva últimas 1h: {chuva} mm."
        )
        return resumo

    except Exception as e:
        return f"Erro de conexão: {e}"


#Recomendação de passeio turístico

def generate_recommendation(clima_summary: str) -> str:
    """
    Recebe o resumo do clima e envia para o modelo GPT da OpenAI
    para gerar uma recomendação de passeio turístico adequada.
    """
    prompt = (
        f"Você é um assistente de turismo. "
        f"Com base na seguinte descrição do clima, recomende um passeio turístico adequado na cidade:\n\n"
        f"{clima_summary}\n\n"
        "Responda de forma curta e amigável."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        recomendacao = response.choices[0].message.content.strip()
        return recomendacao
    except Exception as e:
        return f"Erro ao gerar recomendação: {e}"


#Fluxo principal
def main():
    """
    Função principal que coordena a execução do chatbot ClimaTour:
    1. Recebe o estado do usuário
    2. Obtém cidade representativa
    3. Consulta o clima
    4. Gera recomendação de passeio turístico
    5. Exibe informações no terminal
    """
    print("Olá! Bem-vindo ao ClimaTour.")

    estado = input("Digite o seu estado --> ")

    cidade = get_representative_city(estado)

    clima = get_weather(cidade)
    print("\n" + clima + "\n")

    recomendacao = generate_recommendation(clima)
    print("Sugestão de passeio: ")
    print(recomendacao)

if __name__ == "__main__":
    main()

