import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = ""
OPENAI_API_KEY = ""

client = openai.OpenAI(api_key=OPENAI_API_KEY)

async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    logger.info(f"Mensagem recebida de {user_id}: {user_message}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=100
        )

        reply = response.choices[0].message.content
        logger.info(f"Resposta enviada para {user_id}: {reply}")
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Erro ao processar mensagem de {user_id}: {e}")
        await update.message.reply_text("Ops! Algo deu errado.")

async def oi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Comando /start recebido de {update.effective_user.id}")
    await update.message.reply_text("Oi! Eu sou seu assistente. Como posso ajudar?")

def main():
    logger.info("Inicializando o bot...")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("oi", oi))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    logger.info("Bot iniciado e aguardando mensagens.")
    application.run_polling()

if __name__ == "__main__":
    main()
