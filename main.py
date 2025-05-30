import requests
from bs4 import BeautifulSoup
import time
import telegram

# Configurações do bot
TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
CHAT_ID = "-1002116488128"
bot = telegram.Bot(token=TOKEN)

# Estatísticas
acertos = 0
gales = 0
erros = 0
ultimos_resultados = []

def extrair_resultados():
    url = "https://casinoscores.com/es/bac-bo/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    resultados = []
    entradas = soup.select(".card.rounded.shadow-sm.py-2.px-3.mb-2")
    for entrada in entradas:
        tipo = entrada.select_one('img[alt="Êxito"]')
        if not tipo:
            continue

        resultado_texto = entrada.select_one("div.bac-bo-dice-outcome span.ml-1")
        if not resultado_texto:
            continue

        soma = resultado_texto.text.strip().replace('Σ', '')
        if soma not in ['5', '6', '7']:
            continue

        cor = entrada.select_one('img.mb-1')
        if not cor or "6--7--8.png" not in cor['src']:
            continue  # só continua se for faixa amarela

        resultados.append(soma)

    return resultados

def verificar_sinal():
    global acertos, gales, erros, ultimos_resultados

    novos_resultados = extrair_resultados()
    if not novos_resultados:
        return

    for resultado in novos_resultados:
        if resultado in ultimos_resultados:
            continue  # já tratado

        ultimos_resultados.append(resultado)
        if len(ultimos_resultados) > 20:
            ultimos_resultados = ultimos_resultados[-20:]

        bot.send_message(chat_id=CHAT_ID, text=f"🎯 Entrada encontrada!\nResultado: TIE Σ{resultado} (Amarelo)\n\nEntrar no próximo!")
        time.sleep(120)  # tempo do gale

        novos = extrair_resultados()
        if resultado in novos:
            acertos += 1
            bot.send_message(chat_id=CHAT_ID, text="✅ Acerto de primeira!")
        elif len(novos) > 0 and novos[0] == resultado:
            gales += 1
            bot.send_message(chat_id=CHAT_ID, text="🌀 Acerto no Gale!")
        else:
            erros += 1
            bot.send_message(chat_id=CHAT_ID, text="❌ Erro.")

        # Atualiza estatísticas
        estatisticas = f"""
📊 Estatísticas:
✅ Acertos: {acertos}
🌀 Gales: {gales}
❌ Erros: {erros}
        """
        bot.send_message(chat_id=CHAT_ID, text=estatisticas)

while True:
    try:
        verificar_sinal()
        time.sleep(30)
    except Exception as e:
        print(f"Erro: {e}")
        time.sleep(60)