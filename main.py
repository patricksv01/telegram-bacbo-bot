@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensagem recebida:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        nome_grupo = data["message"]["chat"].get("title", "sem nome")
        print(f"🆔 ID do grupo: {chat_id} | Nome: {nome_grupo}")

        # Opcional: responder para confirmar
        send_message("✅ Bot ativo! Esse é o ID do grupo.")

    return {"ok": True}