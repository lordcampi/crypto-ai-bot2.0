from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from bot import analyze
from config import TELEGRAM_BOT_TOKEN


# -----------------------------
# HANDLER PRINCIPAL
# -----------------------------
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "obtener señal" in text:

        await update.message.reply_text("🏦 Analizando mercado tipo hedge fund...")

        try:

            sig = analyze()

            # 🔥 FIX: asegurar que sea dict
            if isinstance(sig, list):
                sig = sig[0]

            if not sig:
                await update.message.reply_text("⚠️ No hay señal en este momento.")
                return

            msg = f"""
🚀 CRYPTO SIGNAL (EDUCATIONAL)

🪙 Asset: {sig['symbol']}
💰 Price: {sig['price']}

📊 Probability: {sig['probability']}%
⭐ Score: {sig['score']}

🛑 Stop Loss: {sig['stop_loss']}
🎯 Take Profit: {sig['take_profit']}

────────────────────────
⚠️ DISCLAIMER:
Este sistema es solo educativo.
No constituye asesoría financiera ni recomendación de inversión.

────────────────────────
🧠 GESTIÓN DE RIESGO:
- Arriesga máximo 1% a 2% por operación
- Usa siempre Stop Loss
- No operes con emociones (evita FOMO)
- Mantén disciplina

────────────────────────
🟢 RECOMENDACIÓN:
Este sistema está optimizado para SPOT trading.
NO se recomienda usar futuros ni apalancamiento.

────────────────────────
📌 NOTA:
El mercado cripto es altamente volátil.
Las señales no garantizan resultados.
"""

            await update.message.reply_text(msg)

        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")

    else:

        await update.message.reply_text("Escribe: Obtener Señal")


# -----------------------------
# INICIO DEL BOT
# -----------------------------
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, handler))

print("🤖 Bot Hedge Fund activo (educativo)")

app.run_polling()