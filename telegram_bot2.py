#!/usr/bin/env python3

from typing import Final
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler
)
import spacy

# === BOT SETTINGS ===
TOKEN: Final = "8213262393:AAHrkAxL8LiyUFFN5xp4zurFImPaQRaz6-4"
BOT_USERNAME: Final = "@sibondBot"

# === NLP Model (load once globally) ===
nlp = spacy.load("en_core_web_sm")

# === STATES ===
STATE0 = 0

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Greetings! I am Si-Bond, Let's get started😇!"
        "Type freely for quick replies, or begin a guided talk with /startconv."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can chat simply or guide thee in conversation. "
                                    "Use /startconv to begin a stateful dialogue, "
                                    "or just type to get quick replies.")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thanks for the chat. I'll be off then!")
    return ConversationHandler.END


# === SIMPLE REACTIVE RESPONSES (from first bot) ===
def handle_response(text: str) -> str:
    processed = text.lower()

    if "hello" in processed:
        return "Hey there!"
    if "how are you" in processed:
        return "I am good!"
    if "i love python" in processed:
        return "Remember to subscribe 😎"
    return "I do not understand what you wrote..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


# === STATEFUL CONVERSATION (from bot) ===
async def startconv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Begin a conversation"""
    await update.message.reply_text("Thou hast begun a guided conversation. Speak thy mind...")
    return STATE0


async def state0_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Use SpaCy to analyze user input"""
    doc = nlp(update.message.text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    reply = f"I see these nouns in thy speech: {', '.join(nouns)}" if nouns else "I caught no nouns."

    await update.message.reply_text(reply)
    return STATE0  # remain in state for further input


# === MAIN FUNCTION ===
def main():
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Simple commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    # Reactive message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("startconv", startconv)],
        states={
            STATE0: [MessageHandler(filters.TEXT & ~filters.COMMAND, state0_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)]
    )
    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
