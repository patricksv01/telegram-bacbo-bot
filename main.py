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
ultimo_sinal = None

bot = telegram.Bot(token=TOKEN)

# --- FUNÇÃO PARA ENVIAR MENSAGEM ---
def enviar_mensagem(mensagem):
    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="HTML")

# --- FUNÇÃO PRINCIPAL DE MONITORAMENTO ---
def verificar_bacbo():
    global ultimo_sinal, acertos, acertos_gale, erros

    url = "https://www.casinoscores.com/bacbo"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    linhas = soup.find_all("tr")

    for linha in linhas:
        try:
            tie_img = linha.find("img", alt="Êxito")
            if not tie_img:
                continue  # Não é TIE

            dados_span = linha.find("span", class_="ml-2")
            if not dados_span or not dados_span.find("img"):
                continue

            dados_src = dados_span.find("img")["src"]
            # Verifica se é 5, 6 ou 7 no src da imagem
            if not any(num in dados_src for num in ["5", "6", "7"]):
                continue

            # Captura data e hora para evitar duplicatas
            data_tag = linha.find("p", class_="dateTime_DateTime__date__bXWTP")
            hora_tag = linha.find("p", class_="dateTime_DateTime__time__f0_Bn")
            if not data_tag or not hora_tag:
                continue

            data_hora = f"{data_tag.text.strip()} {hora_tag.text.strip()}"

            if data_hora == ultimo_sinal:
                continue  # Já sinalizado

            ultimo_sinal = data_hora

            # Envia sinal no grupo
            enviar_mensagem(f"<b>🎯 SINAL IDENTIFICADO</b>\n"
                            f"TIE com dado Σ5, Σ6 ou Σ7!\n"
                            f"<b>🕒 Horário:</b> {data_hora}\n\n"
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
        verificar_bacbo()
        time.sleep(10)  # A cada 10 segundos