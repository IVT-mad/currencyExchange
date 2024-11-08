from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bs4 import BeautifulSoup
from WEBScrappa import *
from APIRate import *
import datetime
import os

USER_NAME_STATE = 1
EXCHANGE_RATE_STATE = 2
SORT_STATE = 3
SORT_STATE_1 = 4
SORT_STATE1 = 5

# Начало диалога: спрашиваем имя пользователя
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здравствуйте, как я могу к Вам обращаться?")
    context.user_data['state'] = USER_NAME_STATE

# Отправка сообщений более 4096
async def send_long_message(update, message):
    chunk_size = 4096
    for i in range(0, len(message), chunk_size):
        await update.message.reply_text(message[i:i+chunk_size])

# Обрабатываем имя пользователя
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('state') == USER_NAME_STATE:
        user_name = update.message.text
        context.user_data['name'] = user_name
        reply_keyboard = [['Курсы валют - webscrapping с сайта \nЦентрального Банка России', 'Курсы валют - API запрос']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(f"Рад знакомству, {user_name}. Какой вариант желаете выбрать?",
                                        reply_markup=markup)
        context.user_data['state'] = EXCHANGE_RATE_STATE


async def get_rate_from_site(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get('state')
    rate = sort_by_code_webscraping(get_exchange_rates(), ascending=True)

    await update.message.reply_text(f"Курсы валют на {datetime.date.today()}: {rate}")

    reply_keyboard = [
        ['Сортировка УБВ по названию', 'Сортировка ВЗР по названию',
         'Сортировка УБВ по аббревеатуре', 'Сортировка ВЗР по названию',
         'Сортировка УБВ по покупательной способности', 'Сортировка ВЗР по покупательной способности']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Какую сортировку вы хотите применить?", reply_markup=markup)
    context.user_data['state'] = "webscraping_sort"
async def get_rate_from_api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get('state')
    rate = sort_by_rate_api(main(), reverse=True)

    await send_long_message(update, f"Курсы валют: {rate}")

    reply_keyboard = [
        ['Сортировка по коду валюты (по возрастанию)', 'Сортировка по коду валюты (по убыванию)',
         'Сортировка по названию валюты (по возрастанию)', 'Сортировка по названию валюты (по убыванию)',
         'Сортировка по курсу валюты (по возрастанию)', 'Сортировка по курсу валюты (по убыванию)']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Какую сортировку вы хотите применить?", reply_markup=markup)
    context.user_data['state'] = "api_sort"

# Обрабатываем выбор пользователя
async def handle_rate_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    state = context.user_data.get('state', None)
    print(f"Current state: {state}")
    if state == USER_NAME_STATE:
        await handle_name(update, context)
    elif state == EXCHANGE_RATE_STATE:
        if update.message.text == "Курсы валют - webscrapping с сайта \nЦентрального Банка России":
            await get_rate_from_site(update, context)
        elif update.message.text == "Курсы валют - API запрос":
            await get_rate_from_api(update, context)
        else:
            await default_response(update, context)
    elif state == "webscraping_sort":
        if update.message.text == "Сортировка УБВ по названию":
            await send_long_message(update, sort_by_definition_webscraping(get_exchange_rates(), ascending=True))
        elif update.message.text == "Сортировка ВЗР по названию":
            await send_long_message(update, sort_by_definition_webscraping(get_exchange_rates(), ascending=False))
        elif update.message.text == "Сортировка УБВ по аббревеатуре":
            await send_long_message(update, sort_by_code_webscraping(get_exchange_rates(), ascending=True))
        elif update.message.text == "Сортировка ВЗР по аббревеатуре":
            await send_long_message(update, sort_by_code_webscraping(get_exchange_rates(), ascending=False))
        elif update.message.text == "Сортировка УБВ по покупательной способности":
            await send_long_message(update, sort_by_rate_webscraping(get_exchange_rates(), ascending=True))
        elif update.message.text == "Сортировка ВЗР по покупательной способности":
            await send_long_message(update, sort_by_rate_webscraping(get_exchange_rates(), ascending=False))

    elif state == "api_sort":
        if update.message.text == "Сортировка по коду валюты (по возрастанию)":
            await send_long_message(update, sort_by_currency_code_api(main(), reverse=False))
        elif update.message.text == "Сортировка по коду валюты (по убыванию)":
            await send_long_message(update, sort_by_currency_code_api(main(), reverse=True))
        elif update.message.text == "Сортировка по названию валюты (по возрастанию)":
            await send_long_message(update, sort_by_currency_name_api(main(), reverse=False))
        elif update.message.text == "Сортировка по названию валюты (по убыванию)":
            await send_long_message(update, sort_by_currency_name_api(main(), reverse=True))
        elif update.message.text == "Сортировка по курсу валюты (по возрастанию)":
            await send_long_message(update, sort_by_rate_api(main(), reverse=False))
        elif update.message.text == "Сортировка по курсу валюты (по убыванию)":
            await send_long_message(update, sort_by_rate_api(main(), reverse=True))
    elif state == None:
        await default_response(update, context)
    else:
        await default_response(update, context)


# Стандартный ответ для непонятных запросов
async def default_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [['Курсы валют - webscrapping с сайта \nЦентрального Банка России',
                       'Курсы валют - API запрос']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Извините, я не понял ваш запрос. Пожалуйста, выберите один из предложенных вариантов.",
        reply_markup=markup)
    context.user_data['state'] = EXCHANGE_RATE_STATE


# Создаем и настраиваем бота
app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

# Добавляем обработчики
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rate_selection))

# Запускаем бота
app.run_polling()