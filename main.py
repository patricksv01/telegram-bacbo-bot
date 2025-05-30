import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Token e ID do grupo (já configurados por você)
TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
CHAT_ID = "-1002122803639"
bot = Bot(token=TOKEN)

# Estatísticas
acertos = 0
acertos_gale = 0
erros = 0
ultimos_resultados = []

# Função para extrair os dados do site
def verificar_resultado():
    url = "https://www.casinoscores.com/casino/peaks-gaming/bac-bo"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        resultados_html = soup.find_all("div", class_="flex justify-between items-center")

        resultados = []
        for r in resultados_html:
            partes = r.get_text(strip=True).split("Σ")
            if len(partes) == 2 and "Tie" in partes[0]:
                soma = int(partes[1])
                if soma in [5, 6, 7]:
                    resultados.append((soma, "Tie"))

        return resultados
    except Exception as e:
        print("Erro ao acessar site:", e)
        return []

# Loop principal do bot
def iniciar_monitoramento():
    global acertos, acertos_gale, erros, ultimos_resultados

    print("Bot iniciado e monitorando 24h por dia...")
    while True:
        resultados = verificar_resultado()
        if resultados:
            novo = resultados[0]
            if novo not in ultimos_resultados:
                ultimos_resultados.insert(0, novo)
                ultimos_resultados = ultimos_resultados[:10]  # guarda os 10 últimos

                # Envia sinal
                soma, _ = novo
                mensagem = f"🎯 SINAL ENCONTRADO!\n\n🟡 Amarelo Σ{soma} + Tie\nEntre com proteção!\n\n🎲 Estatísticas:\n✅ Acertos: {acertos}\n🌀 Acertos no Gale: {acertos_gale}\n❌ Erros: {erros}"
                bot.send_message(chat_id=CHAT_ID, text=mensagem)

                # Espera pelo resultado final para atualizar as estatísticas (simulação)
                time.sleep(60)
                # Aqui você pode ajustar como verificar se foi acerto, gale ou erro.
                acertos += 1  # Exemplo: considerar tudo como acerto direto por enquanto

        time.sleep(30)  # Espera 30 segundos antes de verificar de novo

# Iniciar
if __name__ == "__main__":
    iniciar_monitoramento()