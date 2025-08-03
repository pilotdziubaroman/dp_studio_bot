
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать в DP Studio! Для доступа к контенту переведите оплату. После подтверждения — вы получите доступ.")

async def request_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "waiting_confirmation"

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Подтвердить оплату", callback_data=f"confirm_{user_id}")
    ]])
    await context.bot.send_message(chat_id=ADMIN_ID,
                                   text=f"Пользователь @{update.effective_user.username} запросил доступ.",
                                   reply_markup=keyboard)
    await update.message.reply_text("Запрос отправлен. Ожидайте подтверждения.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("confirm_") and int(query.from_user.id) == ADMIN_ID:
        user_id = int(data.split("_")[1])
        await context.bot.send_message(chat_id=user_id, text="Оплата подтверждена! Доступ открыт: https://t.me/+uFJK4zMvnuYxMDQy")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("access", request_access))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
