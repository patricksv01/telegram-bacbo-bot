import requests
from bs4 import BeautifulSoup
import time
import telegram

# Configurações do Telegram
TELEGRAM_TOKEN = '8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI'  # Seu token real
CHAT_ID = '-1002121860565'  # Grupo Bac Bo Patrick

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Para evitar mensagens repetidas
sinais_enviados = set()

def extrair_sinais(html):
    sinais = []
    soup = BeautifulSoup(html, 'html.parser')

    botoes = soup.find_all('button', class_='cell--bac_bo')
    for btn in botoes:
        numero = btn.get('data-result')
        tipo = btn.get('data-type')
        hora = btn.get('data-hour')
        minuto = btn.get('data-minute')

        if not (numero and tipo and hora and minuto):
            continue

        numero_int = int(numero)

        # Verifica condição para sinal
        if (numero_int in [5, 6, 7] and tipo in ['player', 'tie']) or (numero_int == 10 and tipo == 'tie'):
            sinal_id = f"{tipo}_{numero}_{hora}_{minuto}"
            sinais.append((sinal_id, numero_int, tipo, hora, minuto))
    return sinais

def buscar_resultados():
    url = 'https://www.casinoscores.com/games/bac-bo'  # Altere se necessário
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('Erro ao buscar dados:', response.status_code)
            return None
    except Exception as e:
        print('Erro na requisição:', e)
        return None

def enviar_mensagem(sinal):
    sinal_id, numero, tipo, hora, minuto = sinal
    mensagem = f"🎯 *SINAL DETECTADO!*\nNúmero: *{numero}*\nTipo: *{tipo.upper()}*\nHorário: *{hora}:{minuto}*"
    print(mensagem)
    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode='Markdown')

def main():
    while True:
        html = buscar_resultados()
        if html:
            sinais = extrair_sinais(html)
            for sinal in sinais:
                sinal_id = sinal[0]
                if sinal_id not in sinais_enviados:
                    enviar_mensagem(sinal)
                    sinais_enviados.add(sinal_id)
        time.sleep(10)  # Checagem a cada 10 segundos

if __name__ == '__main__':
    main()