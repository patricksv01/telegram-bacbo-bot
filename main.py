import requests
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8100745572:AAHFY4gZKnDu6ep8YqgydqkcApcBSUhTnvI"
CHAT_ID = "-1002301941872"
TARGET_NUMBERS = [33, 20, 17, 28, 7, 26, 1, 2, 18, 10]
URL = "https://www.tipminer.com/br/historico/evolution/xxxtreme-lightning-roulette"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"Exceção ao enviar mensagem: {e}")

def get_last_number():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        result_cells = soup.find_all("div", class_="cell__result")
        if not result_cells:
            return None
        last_result = result_cells[-1].get_text(strip=True)
        return int(last_result)
    except Exception as e:
        print(f"Erro ao capturar número: {e}")
        return None

def main():
    last_checked = None
    while True:
        last_number = get_last_number()
        if last_number is not None:
            if last_number != last_checked:
                last_checked = last_number
                if last_number in TARGET_NUMBERS:
                    message = (
                        f"🎰 Número sorteado: <b>{last_number}</b>\n"
                        "⚠️ Estratégia: Entrar na 1ª e 2ª coluna e cobrir o 0."
                    )
                    send_message(message)
                    print(f"Mensagem enviada: {last_number}")
                else:
                    print(f"Número {last_number} não está na lista alvo.")
            else:
                print("Nenhuma nova rodada.")
        else:
            print("Erro ao capturar o último número.")
        time.sleep(60)

if __name__ == "__main__":
    main()