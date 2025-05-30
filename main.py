import requests
from bs4 import BeautifulSoup
import time
import telegram

# === CONFIGURAÇÕES ===
TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
GROUP_ID = -1002080473293  # ID do grupo Bac Bo Patrick

bot = telegram.Bot(token=TOKEN)

# Estatísticas globais
acertos = 0
acertos_gale = 0
erros = 0

# Guarda o último resultado analisado para não repetir
ultimo_resultado = ""

def verificar_resultado():
    global acertos, acertos_gale, erros, ultimo_resultado

    try:
        url = "https://www.casinoscores.com/bacbo"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontra os resultados (último vem primeiro)
        resultados = soup.find_all("td", class_="text-nowrap text-center")
        for td in resultados:
            img = td.find("img", alt="Êxito")
            if not img:
                continue

            # Verifica se é TIE
            if "TIE.png" in img["src"]:
                soma_spans = td.find_all("span", class_="ml-1")
                for span in soma_spans:
                    texto = span.get_text(strip=True)
                    if texto.startswith("Σ") and len(texto) == 3:
                        if texto != ultimo_resultado:
                            ultimo_resultado = texto
                            if texto in ["Σ5", "Σ6", "Σ7"]:
                                acertos += 1
                                bot.send_message(
                                    chat_id=GROUP_ID,
                                    text=f"🎯 SINAL ENCONTRADO!\nSaiu empate {texto} amarelo (TIE)\n\n📊 Estatísticas:\n✅ Acertos: {acertos}\n🟡 Acertos no Gale: {acertos_gale}\n❌ Erros: {erros}"
                                )
                            else:
                                erros += 1
                            return  # só analisa o último resultado

    except Exception as e:
        print("Erro ao verificar resultado:", e)

# Loop contínuo (verifica a cada 60 segundos)
while True:
    verificar_resultado()
    time.sleep(60)  # espera 1 minuto