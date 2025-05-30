from flask import Flask
import requests
from bs4 import BeautifulSoup
import threading
import time
from collections import deque

app = Flask(__name__)

TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
CHAT_ID = "-1002649479196"

acertos_primeira = 0
acertos_gale = 0
erros = 0
ultimos_ids = deque(maxlen=50)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def verificar_site():
    global acertos_primeira, acertos_gale, erros, ultimos_ids
    while True:
        try:
            url = "https://www.tipminer.com/br/historico/blaze/bac-bo?limit=600&timezone=America%2FSao_Paulo"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            botoes = soup.select("button.cell--bac_bo")

            for botao in botoes:
                resultado = botao.get("data-result")
                tipo = botao.get("data-type")
                id_unico = botao.get("data-id")

                if not tipo or not id_unico:
                    continue

                if id_unico in ultimos_ids:
                    continue

                ultimos_ids.append(id_unico)

                if not resultado:
                    resultado_tag = botao.select_one(".cell__result")
                    if resultado_tag:
                        resultado = resultado_tag.get_text(strip=True)

                if not resultado or not resultado.isdigit():
                    continue

                resultado_int = int(resultado)
p
                # Aqui está sua regra para enviar sinal quando tipo == "tie" e resultado em [5,6,7]
                if tipo == "tie" and resultado_int in [5, 6, 7]:
                    acertos_primeira += 1  # Você pode adaptar para tratar acertos_gale e erros conforme quiser
                    total_acertos = acertos_primeira + acertos_gale
                    total = total_acertos + erros
                    porcentagem = round((total_acertos / total) * 100, 2) if total > 0 else 0

                    mensagem = (
                        f"🔴 SINAL DE ENTRADA\n"
                        f"🎲 Resultado: {resultado} Amarelo\n"
                        f"📍 Apostar no VERMELHO até GALE 1\n\n"
                        f"📊 Estatísticas:\n"
                        f"✅ Acertos: {acertos_primeira}\n"
                        f"🟡 Acertos no Gale: {acertos_gale}\n"
                        f"❌ Erros: {erros}\n"
                        f"📈 Porcentagem: {porcentagem}%"
                    )
                    send_message(mensagem)

        except Exception as e:
            print("Erro ao verificar site:", e)

        time.sleep(15)

@app.route("/")
def index():
    return "Bot funcionando!"

@app.route("/teste")
def teste_manual():
    mensagem = (
        "🔴 SINAL DE ENTRADA (TESTE MANUAL)\n"
        "🎲 Resultado: 6 Amarelo\n"
        "📍 Apostar no VERMELHO até GALE 1\n\n"
        "📊 Estatísticas:\n"
        f"✅ Acertos: {acertos_primeira}\n"
        f"🟡 Acertos no Gale: {acertos_gale}\n"
        f"❌ Erros: {erros}\n"
        f"📈 Porcentagem: 100%"
    )
    send_message(mensagem)
    return "✅ Sinal de teste enviado!"

if __name__ == "__main__":
    threading.Thread(target=verificar_site, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
