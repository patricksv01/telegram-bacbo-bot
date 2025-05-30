import requests
from bs4 import BeautifulSoup
import time
import telegram

# --- CONFIGURAÇÕES DO TELEGRAM ---
TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
CHAT_ID = "-1002102628380"  # ID do grupo Bac Bo Patrick

# --- ESTATÍSTICAS ---
acertos = 0
acertos_gale = 0
erros = 0
ultimo_horario = None

bot = telegram.Bot(token=TOKEN)

# --- FUNÇÃO PARA ENVIAR MENSAGEM ---
def enviar_mensagem(mensagem):
    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="HTML")

# --- FUNÇÃO PARA MONITORAR O SITE TIPMINER ---
def verificar_tipminer():
    global ultimo_horario, acertos, acertos_gale, erros

    url = "https://www.tipminer.com/br/historico/jonbet/bac-bo"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    celulas = soup.find_all('div', class_='cell__content')

    for celula in celulas:
        try:
            numero_div = celula.find('div', class_='cell__result')
            hora_div = celula.find('div', class_='cell__date')

            if not numero_div or not hora_div:
                continue

            numero = numero_div.text.strip()
            horario = hora_div.text.strip()

            if numero not in ['5', '6', '7']:
                continue  # Não é número alvo

            if horario == ultimo_horario:
                continue  # Já sinalizado

            ultimo_horario = horario

            # Envia sinal no grupo
            enviar_mensagem(f"<b>🎯 SINAL IDENTIFICADO</b>\n"
                            f"Número amarelo: <b>{numero}</b>\n"
                            f"<b>🕒 Horário:</b> {horario}\n\n"
                            f"🎲 Entrada: <b>TIE</b> (amarelo)\n"
                            f"🎯 Estatísticas:\n"
                            f"✅ Acertos: {acertos}\n"
                            f"🟡 Acertos no Gale: {acertos_gale}\n"
                            f"❌ Erros: {erros}")
            return

        except Exception as e:
            print(f"Erro: {e}")

# --- LOOP PRINCIPAL ---
if __name__ == "__main__":
    while True:
        verificar_tipminer()
        time.sleep(10)  # Verifica a cada 10 segundos