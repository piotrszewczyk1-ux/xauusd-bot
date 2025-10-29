from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# === USTAWIENIA TELEGRAM ===
BOT_TOKEN = "8428959424:AAHtN6ulpgFbI-4nxuU1f5oz67hNVkdkxn8"
CHAT_ID = "7324665959"

def send_telegram_message(msg, parse_mode="Markdown"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": parse_mode
    }
    response = requests.post(url, json=payload)
    print(f"🔎 Kod odpowiedzi: {response.status_code}")
    print(f"🔎 Treść odpowiedzi: {response.text}")
    return response

@app.route("/tv", methods=["POST"])
def tv():
    data = request.get_json(force=True)
    print("✅ Odebrano alert z TradingView:")
    print(data)

    symbol = data.get("symbol", "XAUUSD")
    side = data.get("side", "-")
    price = data.get("price", "-")
    tp = data.get("tp", "-")
    sl = data.get("sl", "-")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if side.upper() == "BUY":
        emoji = "🟢"
        color_text = "*BUY Signal*"
    elif side.upper() == "SELL":
        emoji = "🔴"
        color_text = "*SELL Signal*"
    else:
        emoji = "⚪"
        color_text = "*Sygnał*"

    msg = (
        f"{emoji} {color_text} ({symbol})\n"
        f"💰 Cena wejścia: *{price}*\n"
        f"🎯 TP: *{tp}*\n"
        f"🛑 SL: *{sl}*\n"
        f"📅 Czas: {now}"
    )

    send_telegram_message(msg)

    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
