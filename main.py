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
ultimos_ids = deque(maxlen=100)
sinais_ativos = deque(maxlen=10)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def verificar_site():
    global acertos_primeira, acertos_gale, erros, ultimos_ids, sinais_ativos
    while True:
        try:
            url = "https://www.tipminer.com/br/historico/blaze/bac-bo?limit=600&timezone=America%2FSao_Paulo"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            botoes = soup.select("button.cell--bac_bo")
            botoes.reverse()  # do mais antigo pro mais recente

            historico = []
            for botao in botoes:
                resultado = botao.get("data-result")
                tipo = botao.get("data-type")
                id_unico = botao.get("data-id")

                if not tipo or not id_unico:
                    continue

                if not resultado:
                    resultado_tag = botao.select_one(".cell__result")
                    if resultado_tag:
                        resultado = resultado_tag.get_text(strip=True)

                if not resultado or not resultado.isdigit():
                    continue

                resultado_int = int(resultado)

                historico.append({
                    "id": id_unico,
                    "resultado": resultado_int,
                    "tipo": tipo
                })

            # Verificar se já analisamos
            for i, item in enumerate(historico):
                if item["id"] in ultimos_ids:
                    continue

                ultimos_ids.append(item["id"])

                # SINAL DE ENTRADA
                if item["tipo"] == "tie" and item["resultado"] in [5, 6, 7]:
                    sinais_ativos.append({
                        "index": i,
                        "verificado": False
                    })

                    mensagem = (
                        f"🔴 SINAL DE ENTRADA\n"
                        f"🎲 Resultado: {item['resultado']} Amarelo\n"
                        f"📍 Apostar no VERMELHO até GALE 1\n\n"
                        f"📊 Estatísticas:\n"
                        f"✅ Acertos: {acertos_primeira}\n"
                        f"🟡 Acertos no Gale: {acertos_gale}\n"
                        f"❌ Erros: {erros}"
                    )
                    send_message(mensagem)

            # Verificar sinais ativos
            for sinal in sinais_ativos:
                if sinal["verificado"]:
                    continue
                index = sinal["index"]
                if index + 2 < len(historico):
                    prox1 = historico[index + 1]
                    prox2 = historico[index + 2]
                    if prox1["tipo"] == "red":
                        acertos_primeira += 1
                        resultado_final = "✅ Acertamos de PRIMEIRA!"
                    elif prox2["tipo"] == "red":
                        acertos_gale += 1
                        resultado_final = "🟡 Acertamos no GALE!"
                    else:
                        erros += 1
                        resultado_final = "❌ Não deu... foi ERRO."

                    total_acertos = acertos_primeira + acertos_gale
                    total = total_acertos + erros
                    porcentagem = round((total_acertos / total) * 100, 2) if total > 0 else 0

                    mensagem = (
                        f"📊 RESULTADO DO SINAL\n"
                        f"{resultado_final}\n\n"
                        f"✅ Acertos: {acertos_primeira}\n"
                        f"🟡 Acertos no Gale: {acertos_gale}\n"
                        f"❌ Erros: {erros}\n"
                        f"📈 Porcentagem: {porcentagem}%"
                    )
                    send_message(mensagem)
                    sinal["verificado"] = True

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
        f"✅ Acertos: {acertos_primeira}\n"
        f"🟡 Acertos no Gale: {acertos_gale}\n"
        f"❌ Erros: {erros}"
    )
    send_message(mensagem)
    return "✅ Sinal de teste enviado!"

@app.route("/teste_scraping")
def teste_scraping():
    try:
        url = "https://www.tipminer.com/br/historico/blaze/bac-bo?limit=600&timezone=America%2FSao_Paulo"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        botoes = soup.select("button.cell--bac_bo")
        botoes.reverse()

        historico = []
        for botao in botoes[:5]:  # só os primeiros 5 para teste
            resultado = botao.get("data-result")
            tipo = botao.get("data-type")
            id_unico = botao.get("data-id")
            historico.append({
                "id": id_unico,
                "resultado": resultado,
                "tipo": tipo
            })

        texto = "Primeiros 5 resultados extraídos:\n"
        for i, item in enumerate(historico):
            texto += f"{i+1}: id={item['id']}, resultado={item['resultado']}, tipo={item['tipo']}\n"

        print(texto)
        return texto.replace("\n", "<br>")
    except Exception as e:
        return f"Erro no teste scraping: {e}"

if __name__ == "__main__":
    threading.Thread(target=verificar_site, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
